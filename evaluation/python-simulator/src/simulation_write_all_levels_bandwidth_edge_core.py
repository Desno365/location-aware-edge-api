import multiprocessing
import random
from typing import Dict

import numpy as np
import simpy
from matplotlib import pyplot as plt

from result_container import ResultContainer
from src import default_architecture_parameters
from src.clients.data_producer import DataProducer
from src.processing_units.edge_location_central import EdgeLocationCentral
from src.processing_units.edge_location_city import EdgeLocationCity
from src.processing_units.edge_location_continent import EdgeLocationContinent
from src.processing_units.edge_location_country import EdgeLocationCountry
from src.processing_units.edge_location_district import EdgeLocationDistrict
from src.processing_units.edge_location_territory import EdgeLocationTerritory
from src.processing_units.on_processing_ended_enum import OnProcessingEndedEnum

TOTAL_NUMBER_OF_PRODUCER_CLIENTS = 2000
TOTAL_PACKAGES_PRODUCED_BY_EACH_CLIENT = 2  # Note: each client has a waiting time before producing a new package.
BANDWIDTH_RATIO_RANGE = np.linspace(0.1, 1, 32)  # start, end, num_of_points

CONFIGURATIONS = [{"ratio": i, "type": "edge"} for i in BANDWIDTH_RATIO_RANGE]


def run_configuration(config: Dict) -> ResultContainer:
    ratio = config['ratio']
    print(f"################## Running configuration: {ratio}")

    # Setup the simulation.
    result_container = ResultContainer(simulation_name=str(ratio), simulation_type=config['type'])
    env = simpy.Environment()

    # Setup processes in the simulation.
    if config["type"] == "edge":
        edge_central = EdgeLocationCentral(
            simpy_env=env,
            result_container=result_container,
            name=f'Central',
            is_data_coming_from_first_link=False,
            mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_DISTRICT_CENTRAL,
            std_distance_km=default_architecture_parameters.STD_DISTANCE_DISTRICT_CENTRAL,
            on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,  # Save only here.
        )
        edge_central.start_listening_for_incoming_data()

        edge_continents = []
        for i in range(default_architecture_parameters.NUMBER_OF_CONTINENTS):
            edge_continent = EdgeLocationContinent(
                simpy_env=env,
                result_container=result_container,
                name=f'Continent{i}',
                is_data_coming_from_first_link=False,
                mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_DISTRICT_CONTINENT,
                std_distance_km=default_architecture_parameters.STD_DISTANCE_DISTRICT_CONTINENT,
                on_processing_ended_specification=OnProcessingEndedEnum.DO_NOTHING,  # Otherwise latency is considered for multiple packages since in parallel.
            )
            edge_continent.start_listening_for_incoming_data()
            edge_continents.append(edge_continent)

        edge_countries = []
        for i in range(default_architecture_parameters.NUMBER_OF_COUNTRIES):
            edge_country = EdgeLocationCountry(
                simpy_env=env,
                result_container=result_container,
                name=f'Country{i}',
                is_data_coming_from_first_link=False,
                mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_DISTRICT_COUNTRY,
                std_distance_km=default_architecture_parameters.STD_DISTANCE_DISTRICT_COUNTRY,
                on_processing_ended_specification=OnProcessingEndedEnum.DO_NOTHING,  # Otherwise latency is considered for multiple packages since in parallel.
            )
            edge_country.start_listening_for_incoming_data()
            edge_countries.append(edge_country)

        edge_territories = []
        for i in range(default_architecture_parameters.NUMBER_OF_TERRITORIES):
            edge_territory = EdgeLocationTerritory(
                simpy_env=env,
                result_container=result_container,
                name=f'Territory{i}',
                is_data_coming_from_first_link=False,
                mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_DISTRICT_TERRITORY,
                std_distance_km=default_architecture_parameters.STD_DISTANCE_DISTRICT_TERRITORY,
                on_processing_ended_specification=OnProcessingEndedEnum.DO_NOTHING,  # Otherwise latency is considered for multiple packages since in parallel.
            )
            edge_territory.start_listening_for_incoming_data()
            edge_territories.append(edge_territory)

        edge_cities = []
        for i in range(default_architecture_parameters.NUMBER_OF_CITIES):
            edge_city = EdgeLocationCity(
                simpy_env=env,
                result_container=result_container,
                name=f'City{i}',
                is_data_coming_from_first_link=False,
                mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_DISTRICT_CITY,
                std_distance_km=default_architecture_parameters.STD_DISTANCE_DISTRICT_CITY,
                on_processing_ended_specification=OnProcessingEndedEnum.DO_NOTHING,  # Otherwise latency is considered for multiple packages since in parallel.
                override_bandwidth=ratio * default_architecture_parameters.BANDWIDTH_CAPABILITY_CENTRAL,
            )
            edge_city.start_listening_for_incoming_data()
            edge_cities.append(edge_city)

        edge_receivers = []
        for i in range(default_architecture_parameters.NUMBER_OF_DISTRICTS):
            connected_edge_aggregators = [
                edge_central,
                random.choice(edge_continents),
                random.choice(edge_countries),
                random.choice(edge_territories),
                random.choice(edge_cities)
            ]
            transmissions = [connected_edge_aggregator.get_incoming_transmission() for connected_edge_aggregator in connected_edge_aggregators]
            assert len(transmissions) == 5
            edge_receiver = EdgeLocationDistrict(
                simpy_env=env,
                result_container=result_container,
                name=f'District{i}',
                mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_CLIENT_DISTRICT,
                std_distance_km=default_architecture_parameters.STD_DISTANCE_CLIENT_DISTRICT,
                on_processing_ended_specification=OnProcessingEndedEnum.SEND_TO_AGGREGATOR,
                transmissions_to_aggregators=transmissions,
                override_bandwidth=ratio * default_architecture_parameters.BANDWIDTH_CAPABILITY_CENTRAL,
            )
            edge_receiver.start_listening_for_incoming_data()
            edge_receivers.append(edge_receiver)

        for i in range(TOTAL_NUMBER_OF_PRODUCER_CLIENTS):
            connected_edge_receiver = random.choice(edge_receivers)
            transmission = connected_edge_receiver.get_incoming_transmission()
            data_producer = DataProducer(
                simpy_env=env,
                result_container=result_container,
                name=f'DataProducer{i}',
                transmission_to_data_collector=transmission,
                number_of_packages_to_produce=TOTAL_PACKAGES_PRODUCED_BY_EACH_CLIENT
            )
            data_producer.start_producing_data()
    elif config["type"] == "cloud":  # If cloud, setup the cloud and data_producers
        cloud = EdgeLocationCentral(
            simpy_env=env,
            result_container=result_container,
            name="Cloud",
            is_data_coming_from_first_link=True,
            mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_CLIENT_CENTRAL,
            std_distance_km=default_architecture_parameters.STD_DISTANCE_CLIENT_CENTRAL,
            on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
        )
        cloud.start_listening_for_incoming_data()

        for i in range(TOTAL_NUMBER_OF_PRODUCER_CLIENTS):
            transmission = cloud.get_incoming_transmission()
            data_producer = DataProducer(
                simpy_env=env,
                result_container=result_container,
                name=f'DataProducer{i}',
                transmission_to_data_collector=transmission,
                number_of_packages_to_produce=TOTAL_PACKAGES_PRODUCED_BY_EACH_CLIENT
            )
            data_producer.start_producing_data()
    else:
        raise Exception('Type not recognized')

    # Run simulation.
    env.run()

    result_container.print_result(should_total_be_equal_to_sum_of_parts=False)  # Total latency not equal to sum of parts because data sent to multiple aggregators in parallel.
    return result_container


pool = multiprocessing.Pool()
results = pool.map(run_configuration, CONFIGURATIONS)

# Prepare plot variables
total_latencies = np.array([result.get_average_total_latency() for result in results])
total_latencies_confidence = np.array([result.get_average_total_latency_confidence() for result in results])
print(total_latencies_confidence)
x_positions = [i for i in BANDWIDTH_RATIO_RANGE]

# Plot total latency.
plt.figure(figsize=(8, 6))
plt.title('Write Latencies')
plt.plot(x_positions, total_latencies, color="green")
plt.axes().set_ylim([0, None])
plt.ylabel("Average Write Latency")
plt.show()

'''
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title('Write Latencies')
ax.set_ylabel('Average Write Latency')
ax.plot(x_positions, total_latencies, color="green")
ax.fill_between(x_positions, (total_latencies - total_latencies_confidence), (total_latencies + total_latencies_confidence), color="green", alpha=0.1)
ax.set_ylim([0, None])
fig.tight_layout()
'''
