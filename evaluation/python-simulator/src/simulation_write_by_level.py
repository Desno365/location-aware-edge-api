import multiprocessing
import random
from typing import Dict

import numpy as np
import simpy
from matplotlib import pyplot as plt

from src.clients.data_producer_client import DataProducerClient
from result_container import ResultContainer
from src import default_architecture_parameters
from src.processing_units.processing_location_central import ProcessingLocationCentral
from src.processing_units.processing_location_city import ProcessingLocationCity
from src.processing_units.processing_location_continent import ProcessingLocationContinent
from src.processing_units.processing_location_country import ProcessingLocationCountry
from src.processing_units.processing_location_district import ProcessingLocationDistrict
from src.processing_units.processing_location_territory import ProcessingLocationTerritory
from src.processing_units.on_processing_ended_enum import OnProcessingEndedEnum

'''
https://www.cloudping.info/

# Parameters of the edge locations, assuming to have available the Cloudflare network.
# The Cloudflare network at the end of 2021 reports that it has:
# 250 locations,
# 100 Tbps of global network capacity,
# 50 ms put_with_latency from 95% of the world’s Internet-connected population

# Traditional databases and stateful infrastructure usually require you to think about geographical "regions",
# so that you can be sure to store data close to where it is used.
# Thinking about regions can often be an unnatural burden, especially for applications that are not inherently geographical.


When a device's user performs a search, the device sends this information so that it can be preprocessed by a machine learning model and then used to create a list of trending argument per area.

Cloud: the server must know the region the device is in, this information could be retrieved from the IP address but it's not a reliable method.
There are many people out there who believe that IP addresses are given out by area but they are not.
In these days where there are no more usable IP addresses users can also find themselves given a different IP address that the Geo-IP providers have previously located in a different region.
Another method to get the location is by sending it manually, so the device would have to ask the location permission, but this is not privacy friendly.
Periodically the server can perform a trending calculation on the searches performed and saving it locally.
Devices can then retrieve on the cloud the trending results of a particular region.

Edge: through a DNS system the device can send the search information to the nearest (or almost nearest) edge location,
the edge location saves this data in the upper areas.
The areas can periodically perform a trending calculation on their data (that is relative only to that particular area).
Devices can retrieve from the area the trending result of that area.
'''

'''
General use case:
Computation performed locally + geographical aggregation

Then it can become:
- Only geographical aggregation
- Only computation performed locally (ex: publishing videos on social network to avoid modded client)
'''

TOTAL_NUMBER_OF_PRODUCER_CLIENTS = 2000
TOTAL_PACKAGES_PRODUCED_BY_EACH_CLIENT = 3  # Note: each client has a waiting time before producing a new package.

CONFIGURATIONS = [
    {
        "configuration_name": "City Aggregation",
        "type": "edge",
        "aggregation_level": "city",
        "#edge_receivers": default_architecture_parameters.NUMBER_OF_DISTRICTS,
        "#edge_aggregators": default_architecture_parameters.NUMBER_OF_CITIES,
        "mean_distance_producer_receiver": default_architecture_parameters.MEAN_DISTANCE_CLIENT_DISTRICT,
        "std_distance_producer_receiver": default_architecture_parameters.STD_DISTANCE_CLIENT_DISTRICT,
        "mean_distance_receiver_aggregator": default_architecture_parameters.MEAN_DISTANCE_DISTRICT_CITY,
        "std_distance_receiver_aggregator": default_architecture_parameters.STD_DISTANCE_DISTRICT_CITY,
    },
    {
        "configuration_name": "Territory Aggregation",
        "type": "edge",
        "aggregation_level": "territory",
        "#edge_receivers": default_architecture_parameters.NUMBER_OF_DISTRICTS,
        "#edge_aggregators": default_architecture_parameters.NUMBER_OF_TERRITORIES,
        "mean_distance_producer_receiver": default_architecture_parameters.MEAN_DISTANCE_CLIENT_DISTRICT,
        "std_distance_producer_receiver": default_architecture_parameters.STD_DISTANCE_CLIENT_DISTRICT,
        "mean_distance_receiver_aggregator": default_architecture_parameters.MEAN_DISTANCE_DISTRICT_TERRITORY,
        "std_distance_receiver_aggregator": default_architecture_parameters.STD_DISTANCE_DISTRICT_TERRITORY,
    },
    {
        "configuration_name": "Country Aggregation",
        "type": "edge",
        "aggregation_level": "country",
        "#edge_receivers": default_architecture_parameters.NUMBER_OF_DISTRICTS,
        "#edge_aggregators": default_architecture_parameters.NUMBER_OF_COUNTRIES,
        "mean_distance_producer_receiver": default_architecture_parameters.MEAN_DISTANCE_CLIENT_DISTRICT,
        "std_distance_producer_receiver": default_architecture_parameters.STD_DISTANCE_CLIENT_DISTRICT,
        "mean_distance_receiver_aggregator": default_architecture_parameters.MEAN_DISTANCE_DISTRICT_COUNTRY,
        "std_distance_receiver_aggregator": default_architecture_parameters.STD_DISTANCE_DISTRICT_COUNTRY,
    },
    {
        "configuration_name": "Continent Aggregation",
        "type": "edge",
        "aggregation_level": "continent",
        "#edge_receivers": default_architecture_parameters.NUMBER_OF_DISTRICTS,
        "#edge_aggregators": default_architecture_parameters.NUMBER_OF_CONTINENTS,
        "mean_distance_producer_receiver": default_architecture_parameters.MEAN_DISTANCE_CLIENT_DISTRICT,
        "std_distance_producer_receiver": default_architecture_parameters.STD_DISTANCE_CLIENT_DISTRICT,
        "mean_distance_receiver_aggregator": default_architecture_parameters.MEAN_DISTANCE_DISTRICT_CONTINENT,
        "std_distance_receiver_aggregator": default_architecture_parameters.STD_DISTANCE_DISTRICT_CONTINENT,
    },
    {
        "configuration_name": "Central Aggregation",
        "type": "edge",
        "aggregation_level": "central",
        "#edge_receivers": default_architecture_parameters.NUMBER_OF_DISTRICTS,
        "#edge_aggregators": 1,
        "mean_distance_producer_receiver": default_architecture_parameters.MEAN_DISTANCE_CLIENT_DISTRICT,
        "std_distance_producer_receiver": default_architecture_parameters.STD_DISTANCE_CLIENT_DISTRICT,
        "mean_distance_receiver_aggregator": default_architecture_parameters.MEAN_DISTANCE_DISTRICT_CENTRAL,
        "std_distance_receiver_aggregator": default_architecture_parameters.STD_DISTANCE_DISTRICT_CENTRAL,
    },
    {
        "configuration_name": "Cloud solution",
        "type": "cloud",
        "mean_distance_receiver_cloud": default_architecture_parameters.MEAN_DISTANCE_CLIENT_CENTRAL,
        "std_distance_receiver_cloud": default_architecture_parameters.STD_DISTANCE_CLIENT_CENTRAL,
    },
]


def run_configuration(config: Dict) -> ResultContainer:
    print(f"################## Running configuration: {config['configuration_name']}")

    # Setup the simulation.
    result_container = ResultContainer(simulation_name=config['configuration_name'], simulation_type=config['type'])
    env = simpy.Environment()

    # Setup processes in the simulation.
    if config["type"] == "edge":  # If edge, setup edge_aggregators, edge_receivers and data_producers
        edge_aggregators = []
        for i in range(config["#edge_aggregators"]):
            if config["aggregation_level"] == "city":
                edge_aggregator = ProcessingLocationCity(
                    simpy_env=env,
                    result_container=result_container,
                    name=f'EdgeAggregator{i}',
                    is_data_coming_from_first_link=False,
                    mean_distance_km=config['mean_distance_receiver_aggregator'],
                    std_distance_km=config['std_distance_receiver_aggregator'],
                    on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
                )
            elif config["aggregation_level"] == "territory":
                edge_aggregator = ProcessingLocationTerritory(
                    simpy_env=env,
                    result_container=result_container,
                    name=f'EdgeAggregator{i}',
                    is_data_coming_from_first_link=False,
                    mean_distance_km=config['mean_distance_receiver_aggregator'],
                    std_distance_km=config['std_distance_receiver_aggregator'],
                    on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
                )
            elif config["aggregation_level"] == "country":
                edge_aggregator = ProcessingLocationCountry(
                    simpy_env=env,
                    result_container=result_container,
                    name=f'EdgeAggregator{i}',
                    is_data_coming_from_first_link=False,
                    mean_distance_km=config['mean_distance_receiver_aggregator'],
                    std_distance_km=config['std_distance_receiver_aggregator'],
                    on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
                )
            elif config["aggregation_level"] == "continent":
                edge_aggregator = ProcessingLocationContinent(
                    simpy_env=env,
                    result_container=result_container,
                    name=f'EdgeAggregator{i}',
                    is_data_coming_from_first_link=False,
                    mean_distance_km=config['mean_distance_receiver_aggregator'],
                    std_distance_km=config['std_distance_receiver_aggregator'],
                    on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
                )
            elif config["aggregation_level"] == "central":
                edge_aggregator = ProcessingLocationCentral(
                    simpy_env=env,
                    result_container=result_container,
                    name=f'EdgeAggregator{i}',
                    is_data_coming_from_first_link=False,
                    mean_distance_km=config['mean_distance_receiver_aggregator'],
                    std_distance_km=config['std_distance_receiver_aggregator'],
                    on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
                )
            else:
                raise Exception('Aggregation not recognized')
            edge_aggregator.start_listening_for_incoming_data()
            edge_aggregators.append(edge_aggregator)

        edge_receivers = []
        for i in range(config["#edge_receivers"]):
            connected_edge_aggregator = random.choice(edge_aggregators)
            transmission = connected_edge_aggregator.get_incoming_transmission()
            edge_receiver = ProcessingLocationDistrict(
                simpy_env=env,
                result_container=result_container,
                name=f'EdgeReceiver{i}',
                mean_distance_km=config['mean_distance_producer_receiver'],
                std_distance_km=config['std_distance_producer_receiver'],
                on_processing_ended_specification=OnProcessingEndedEnum.SEND_TO_AGGREGATOR,
                transmissions_to_aggregators=[transmission],
            )
            edge_receiver.start_listening_for_incoming_data()
            edge_receivers.append(edge_receiver)

        for i in range(TOTAL_NUMBER_OF_PRODUCER_CLIENTS):
            connected_edge_receiver = random.choice(edge_receivers)
            transmission = connected_edge_receiver.get_incoming_transmission()
            data_producer = DataProducerClient(
                simpy_env=env,
                result_container=result_container,
                name=f'DataProducerClient{i}',
                transmission_to_data_collector=transmission,
                number_of_packages_to_produce=TOTAL_PACKAGES_PRODUCED_BY_EACH_CLIENT,
            )
            data_producer.start_producing_data()
    elif config["type"] == "cloud":  # If cloud, setup the cloud and data_producers
        cloud = ProcessingLocationCentral(
            simpy_env=env,
            result_container=result_container,
            name="Cloud",
            is_data_coming_from_first_link=True,
            mean_distance_km=config['mean_distance_receiver_cloud'],
            std_distance_km=config['std_distance_receiver_cloud'],
            on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
        )
        cloud.start_listening_for_incoming_data()

        for i in range(TOTAL_NUMBER_OF_PRODUCER_CLIENTS):
            transmission = cloud.get_incoming_transmission()
            data_producer = DataProducerClient(
                simpy_env=env,
                result_container=result_container,
                name=f'DataProducerClient{i}',
                transmission_to_data_collector=transmission,
                number_of_packages_to_produce=TOTAL_PACKAGES_PRODUCED_BY_EACH_CLIENT,
            )
            data_producer.start_producing_data()
    else:
        raise Exception('Type not recognized')

    # Run simulation.
    env.run()

    result_container.print_result()
    return result_container


pool = multiprocessing.Pool()
results = pool.map(run_configuration, CONFIGURATIONS)

# Prepare plot variables
total_latencies = [result.get_average_total_latency() for result in results]
first_link_latencies = [result.get_average_first_link_latency() for result in results]
first_processing_latencies = [result.get_average_first_processing_latency() for result in results]
second_link_latencies = [result.get_average_second_link_latency() for result in results]
second_processing_latencies = [result.get_average_second_processing_latency() for result in results]
first_traffic_per_distance = [result.get_total_first_link_traffic_per_distance() for result in results]
second_traffic_per_distance = [result.get_total_second_link_traffic_per_distance() for result in results]
names = [result.simulation_name.replace(" ", "\n") for result in results]
colors = ['green' if result.simulation_type == 'edge' else 'red' for result in results]
x_positions = (range(len(results)))

# Plot total latency.
plt.figure(figsize=(8, 6))
plt.title('Write Latencies')
plt.bar(x_positions, total_latencies, color=colors)
plt.axes().yaxis.grid()  # horizontal lines
plt.xticks(x_positions, names)
plt.ylabel("Average Write Latency")
plt.tight_layout()
plt.show()

# Plot sum of latencies.
plt.figure(figsize=(8, 6))
plt.title('Write Latencies in details')
bars1 = first_link_latencies
bars2 = first_processing_latencies
bars3 = second_link_latencies
bars4 = second_processing_latencies
bars_1_plus_2 = np.add(bars1, bars2).tolist()
bars_1_plus_2_plus_3 = np.add(bars_1_plus_2, bars3).tolist()
plt.bar(x_positions, bars1, color='#333333')
plt.bar(x_positions, bars2, bottom=bars1, color='#7f6d5f')
plt.bar(x_positions, bars3, bottom=bars_1_plus_2, color='#2d7f5e')
plt.bar(x_positions, bars4, bottom=bars_1_plus_2_plus_3, color='#34e363')
plt.xticks(x_positions, names)
plt.ylabel("Average Write Latency")
plt.legend(["First link", "Processing", "Second Link", "Aggregation"])
plt.tight_layout()
plt.show()

# Plot sum of traffic uncut.
plt.figure(figsize=(8, 6))
plt.title('Traffic * Distance')
bars1 = first_traffic_per_distance
bars2 = second_traffic_per_distance
plt.bar(x_positions, bars1, color='#333333')
plt.bar(x_positions, bars2, bottom=bars1, color='#2d7f5e')
plt.xticks(x_positions, names)
plt.ylabel("Total (traffic in MB) * (distance in Km)")
plt.legend(["First link", "Second Link"])
plt.tight_layout()
plt.show()

# Plot sum of traffic cut.
plt.figure(figsize=(8, 6))
cut_limit = int(1.5 * (first_traffic_per_distance[-2] + second_traffic_per_distance[-2]))
plt.title(f'Traffic * Distance (cut at {cut_limit})')
bars1 = first_traffic_per_distance
bars2 = second_traffic_per_distance
plt.bar(x_positions, bars1, color='#333333')
plt.bar(x_positions, bars2, bottom=bars1, color='#2d7f5e')
plt.axes().set_ylim([None, cut_limit])
plt.xticks(x_positions, names)
plt.ylabel("Total (traffic in MB) * (distance in Km)")
plt.legend(["First link", "Second Link"])
plt.tight_layout()
plt.show()
