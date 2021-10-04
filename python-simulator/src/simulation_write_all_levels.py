import multiprocessing
import random
from typing import Dict

import numpy as np
import simpy
from matplotlib import pyplot as plt

from src.clients.data_producer import DataProducer
from result_container import ResultContainer
from src import architecture_parameters
from src.processing_units.edge_location_central import EdgeLocationCentral
from src.processing_units.edge_location_city import EdgeLocationCity
from src.processing_units.edge_location_continent import EdgeLocationContinent
from src.processing_units.edge_location_country import EdgeLocationCountry
from src.processing_units.edge_location_district import EdgeLocationDistrict
from src.processing_units.edge_location_territory import EdgeLocationTerritory
from src.processing_units.on_processing_ended_enum import OnProcessingEndedEnum

SIMULATION_DURATION = 2*60*1000  # In milliseconds.
TOTAL_NUMBER_OF_PRODUCER_CLIENTS = 10000

CONFIGURATIONS = [
    {
        "name": "With the Edge",
        "type": "edge",
    },
    {
        "name": "Cloud",
        "type": "cloud",
    },
]


def run_configuration(config: Dict) -> ResultContainer:
    print(f"################## Running configuration: {config['name']}")

    # Setup the simulation.
    result_container = ResultContainer(simulation_name=config['name'], simulation_type=config['type'])
    env = simpy.Environment()

    # Setup processes in the simulation.
    if config["type"] == "edge":
        edge_central = EdgeLocationCentral(
            simpy_env=env,
            result_container=result_container,
            name=f'Central',
            is_data_coming_from_first_link=False,
            mean_distance_km=architecture_parameters.MEAN_DISTANCE_DISTRICT_CENTRAL,
            std_distance_km=architecture_parameters.STD_DISTANCE_DISTRICT_CENTRAL,
            on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,  # Save only here.
        )
        edge_central.start_listening_for_incoming_data()

        edge_continents = []
        for i in range(architecture_parameters.NUMBER_OF_CONTINENTS):
            edge_continent = EdgeLocationContinent(
                simpy_env=env,
                result_container=result_container,
                name=f'Continent{i}',
                is_data_coming_from_first_link=False,
                mean_distance_km=architecture_parameters.MEAN_DISTANCE_DISTRICT_CONTINENT,
                std_distance_km=architecture_parameters.STD_DISTANCE_DISTRICT_CONTINENT,
                on_processing_ended_specification=OnProcessingEndedEnum.DO_NOTHING,  # Otherwise latency is considered for multiple packages since in parallel.
            )
            edge_continent.start_listening_for_incoming_data()
            edge_continents.append(edge_continent)

        edge_countries = []
        for i in range(architecture_parameters.NUMBER_OF_COUNTRIES):
            edge_country = EdgeLocationCountry(
                simpy_env=env,
                result_container=result_container,
                name=f'Country{i}',
                is_data_coming_from_first_link=False,
                mean_distance_km=architecture_parameters.MEAN_DISTANCE_DISTRICT_COUNTRY,
                std_distance_km=architecture_parameters.STD_DISTANCE_DISTRICT_COUNTRY,
                on_processing_ended_specification=OnProcessingEndedEnum.DO_NOTHING,  # Otherwise latency is considered for multiple packages since in parallel.
            )
            edge_country.start_listening_for_incoming_data()
            edge_countries.append(edge_country)

        edge_territories = []
        for i in range(architecture_parameters.NUMBER_OF_TERRITORIES):
            edge_territory = EdgeLocationTerritory(
                simpy_env=env,
                result_container=result_container,
                name=f'Territory{i}',
                is_data_coming_from_first_link=False,
                mean_distance_km=architecture_parameters.MEAN_DISTANCE_DISTRICT_TERRITORY,
                std_distance_km=architecture_parameters.STD_DISTANCE_DISTRICT_TERRITORY,
                on_processing_ended_specification=OnProcessingEndedEnum.DO_NOTHING,  # Otherwise latency is considered for multiple packages since in parallel.
            )
            edge_territory.start_listening_for_incoming_data()
            edge_territories.append(edge_territory)

        edge_cities = []
        for i in range(architecture_parameters.NUMBER_OF_CITIES):
            edge_city = EdgeLocationCity(
                simpy_env=env,
                result_container=result_container,
                name=f'City{i}',
                is_data_coming_from_first_link=False,
                mean_distance_km=architecture_parameters.MEAN_DISTANCE_DISTRICT_CITY,
                std_distance_km=architecture_parameters.STD_DISTANCE_DISTRICT_CITY,
                on_processing_ended_specification=OnProcessingEndedEnum.DO_NOTHING,  # Otherwise latency is considered for multiple packages since in parallel.
            )
            edge_city.start_listening_for_incoming_data()
            edge_cities.append(edge_city)

        edge_receivers = []
        for i in range(architecture_parameters.NUMBER_OF_DISTRICTS):
            connected_edge_aggregators = []
            connected_edge_aggregators.append(edge_central)
            connected_edge_aggregators.append(random.choice(edge_continents))
            connected_edge_aggregators.append(random.choice(edge_countries))
            connected_edge_aggregators.append(random.choice(edge_territories))
            connected_edge_aggregators.append(random.choice(edge_cities))
            transmissions = [connected_edge_aggregator.get_incoming_transmission() for connected_edge_aggregator in connected_edge_aggregators]
            edge_receiver = EdgeLocationDistrict(
                simpy_env=env,
                result_container=result_container,
                name=f'District{i}',
                mean_distance_km=architecture_parameters.MEAN_DISTANCE_CLIENT_DISTRICT,
                std_distance_km=architecture_parameters.STD_DISTANCE_CLIENT_DISTRICT,
                on_processing_ended_specification=OnProcessingEndedEnum.SEND_TO_AGGREGATOR,
                transmissions_to_aggregators=transmissions,
            )
            edge_receiver.start_listening_for_incoming_data()
            edge_receivers.append(edge_receiver)

        for i in range(TOTAL_NUMBER_OF_PRODUCER_CLIENTS):
            connected_edge_receiver = random.choice(edge_receivers)
            transmission = connected_edge_receiver.get_incoming_transmission()
            data_producer = DataProducer(simpy_env=env, result_container=result_container, name=f'DataProducer{i}', transmission_to_data_collector=transmission)
            data_producer.start_producing_data()
    elif config["type"] == "cloud":  # If cloud, setup the cloud and data_producers
        cloud = EdgeLocationCentral(
            simpy_env=env,
            result_container=result_container,
            name="Cloud",
            is_data_coming_from_first_link=True,
            mean_distance_km=architecture_parameters.MEAN_DISTANCE_CLIENT_CENTRAL,
            std_distance_km=architecture_parameters.STD_DISTANCE_CLIENT_CENTRAL,
            on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
        )
        cloud.start_listening_for_incoming_data()

        for i in range(TOTAL_NUMBER_OF_PRODUCER_CLIENTS):
            transmission = cloud.get_incoming_transmission()
            data_producer = DataProducer(simpy_env=env, result_container=result_container, name=f'DataProducer{i}', transmission_to_data_collector=transmission)
            data_producer.start_producing_data()
    else:
        raise Exception('Type not recognized')

    # Run simulation.
    env.run(until=SIMULATION_DURATION)

    result_container.print_result(should_total_be_equal_to_sum_of_parts=False)  # Total latency not equal to sum of parts because data sent to multiple aggregators in parallel.
    return result_container


pool = multiprocessing.Pool()
results = pool.map(run_configuration, CONFIGURATIONS)

# Prepare plot variables
total_latencies = [result.get_average_total_latency() for result in results]
first_traffic_per_distance = [result.get_average_first_link_traffic_per_distance() for result in results]
second_traffic_per_distance = [result.get_average_second_link_traffic_per_distance() for result in results]
names = [result.simulation_name for result in results]
colors = ['green' if result.simulation_type == 'edge' else 'red' for result in results]
x_positions = (range(len(results)))

# Plot total latency.
plt.figure(figsize=(8, 6))
plt.title('Write Latencies')
plt.bar(x_positions, total_latencies, color=colors)
plt.axes().yaxis.grid()  # horizontal lines
plt.xticks(x_positions, names)
plt.ylabel("Average Write Latency")
plt.show()

# Plot sum of traffic uncut.
plt.figure(figsize=(8, 6))
plt.title('Traffic * Distance')
bars1 = first_traffic_per_distance
bars2 = second_traffic_per_distance
plt.bar(x_positions, bars1, color='#7f6d5f')
plt.bar(x_positions, bars2, bottom=bars1, color='#557f2d')
plt.xticks(x_positions, names)
plt.ylabel("Average Traffic in MB * distance in Km")
plt.legend(["First link", "Second Link"])
plt.show()

# Plot sum of traffic cut.
plt.figure(figsize=(8, 6))
cut_limit = int(1.5 * (first_traffic_per_distance[-2] + second_traffic_per_distance[-2]))
plt.title(f'Traffic * Distance (cut at {cut_limit})')
bars1 = first_traffic_per_distance
bars2 = second_traffic_per_distance
plt.bar(x_positions, bars1, color='#7f6d5f')
plt.bar(x_positions, bars2, bottom=bars1, color='#557f2d')
plt.axes().set_ylim([None, cut_limit])
plt.xticks(x_positions, names)
plt.ylabel("Average Traffic in MB * distance in Km")
plt.legend(["First link", "Second Link"])
plt.show()
