import multiprocessing
import random
from typing import Dict

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

TOTAL_PACKAGES_PRODUCED_BY_EACH_CLIENT = 2  # Note: each client has a waiting time before producing a new package.
CLIENTS_DISTRICTS_RATIO_RANGE = range(1, 402, 26)  # start, end, step
print(CLIENTS_DISTRICTS_RATIO_RANGE)

CONFIGURATIONS_EDGE = [{"ratio": i, "type": "edge"} for i in CLIENTS_DISTRICTS_RATIO_RANGE]
CONFIGURATIONS_CLOUD = [{"ratio": i, "type": "cloud"} for i in CLIENTS_DISTRICTS_RATIO_RANGE]


def run_configuration(config: Dict) -> ResultContainer:
    ratio = config['ratio']
    number_of_clients = default_architecture_parameters.NUMBER_OF_DISTRICTS * ratio
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
            )
            edge_receiver.start_listening_for_incoming_data()
            edge_receivers.append(edge_receiver)

        for i in range(number_of_clients):
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

        for i in range(number_of_clients):
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
results_edge = pool.map(run_configuration, CONFIGURATIONS_EDGE)

pool = multiprocessing.Pool()
results_cloud = pool.map(run_configuration, CONFIGURATIONS_CLOUD)

# Prepare plot variables
total_latencies_edge = [result.get_average_total_latency() for result in results_edge]
total_latencies_cloud = [result.get_average_total_latency() for result in results_cloud]
total_traffic_per_distance_edge = [result.get_total_first_link_traffic_per_distance() + result.get_total_second_link_traffic_per_distance() for result in results_edge]
total_traffic_per_distance_cloud = [result.get_total_first_link_traffic_per_distance() + result.get_total_second_link_traffic_per_distance() for result in results_cloud]
x_positions = [i for i in CLIENTS_DISTRICTS_RATIO_RANGE]

# Plot total latency.
plt.figure(figsize=(8, 6))
plt.title('Write Latencies')
plt.plot(x_positions, total_latencies_edge, color="green")
plt.plot(x_positions, total_latencies_cloud, color="red")
plt.axes().set_ylim([0, None])
plt.ylabel("Average Write Latency")
plt.show()

# Plot sum of traffic uncut.
plt.figure(figsize=(8, 6))
plt.title('Traffic * Distance')
plt.plot(x_positions, total_traffic_per_distance_edge, color="green")
plt.plot(x_positions, total_traffic_per_distance_cloud, color="red")
plt.axes().set_ylim([0, None])
plt.ylabel("Total (traffic in MB) * (distance in Km)")
plt.show()
