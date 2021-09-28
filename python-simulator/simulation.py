import multiprocessing
import random
from typing import Dict

import simpy

from cloud_receiver_and_aggregator import CloudReceiverAndAggregator
from data_producer import DataProducer
from edge_aggregator import EdgeAggregator
from edge_receiver import EdgeReceiver
from results_container import ResultsContainer

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

SIMULATION_DURATION = 2*60*1000  # In milliseconds.
RANDOM_SEED = 42
TOTAL_NUMBER_OF_PRODUCER_CLIENTS = 10000

CONFIGURATIONS = [
    {
        "configuration_name": "City Aggregation",
        "type": "edge",
        "#edge_receivers": 5000,
        "#edge_aggregators": 1000,
        "mean_distance_producer_receiver": 5.0,
        "std_distance_producer_receiver": 2.0,
        "mean_distance_receiver_aggregator": 20.0,
        "std_distance_receiver_aggregator": 7.0,
    },
    {
        "configuration_name": "Territory Aggregation",
        "type": "edge",
        "#edge_receivers": 5000,
        "#edge_aggregators": 400,
        "mean_distance_producer_receiver": 5.0,
        "std_distance_producer_receiver": 2.0,
        "mean_distance_receiver_aggregator": 300.0,
        "std_distance_receiver_aggregator": 100.0,
    },
    {
        "configuration_name": "Country Aggregation",
        "type": "edge",
        "#edge_receivers": 5000,
        "#edge_aggregators": 150,
        "mean_distance_producer_receiver": 5.0,
        "std_distance_producer_receiver": 2.0,
        "mean_distance_receiver_aggregator": 700.0,
        "std_distance_receiver_aggregator": 300.0,
    },
    {
        "configuration_name": "Continent Aggregation",
        "type": "edge",
        "#edge_receivers": 5000,
        "#edge_aggregators": 7,
        "mean_distance_producer_receiver": 5.0,
        "std_distance_producer_receiver": 2.0,
        "mean_distance_receiver_aggregator": 1500.0,
        "std_distance_receiver_aggregator": 500.0,
    },
    {
        "configuration_name": "Central Aggregation",
        "type": "edge",
        "#edge_receivers": 5000,
        "#edge_aggregators": 1,
        "mean_distance_producer_receiver": 5.0,
        "std_distance_producer_receiver": 2.0,
        "mean_distance_receiver_aggregator": 5000.0,
        "std_distance_receiver_aggregator": 2000.0,
    },
    {
        "configuration_name": "Cloud solution",
        "type": "cloud",
        "mean_distance_receiver_cloud": 5000.0,
        "std_distance_receiver_cloud": 2000.0,
    },
]


def run_configuration(config: Dict) -> ResultsContainer:
    print(f"################## Running configuration: {config['configuration_name']}")

    # Setup the simulation.
    results_container = ResultsContainer(config['configuration_name'])
    random.seed(RANDOM_SEED)
    env = simpy.Environment()

    # Setup processes in the simulation.
    if config["type"] == "edge":  # If edge, setup edge_aggregators, edge_receivers and data_producers
        edge_aggregators = []
        for i in range(config["#edge_aggregators"]):
            edge_aggregator = EdgeAggregator(simpy_env=env, results_container=results_container, name=f'EdgeAggregator{i}', mean_distance_km=config['mean_distance_receiver_aggregator'], std_distance_km=config['std_distance_receiver_aggregator'])
            edge_aggregator.start_listening_for_incoming_data()
            edge_aggregators.append(edge_aggregator)

        edge_receivers = []
        for i in range(config["#edge_receivers"]):
            connected_edge_aggregator = random.choice(edge_aggregators)
            transmission = connected_edge_aggregator.get_incoming_transmission()
            edge_receiver = EdgeReceiver(simpy_env=env, results_container=results_container, name=f'EdgeReceiver{i}', transmission_to_aggregator=transmission,  mean_distance_km=config['mean_distance_producer_receiver'], std_distance_km=config['std_distance_producer_receiver'])
            edge_receiver.start_listening_for_incoming_data()
            edge_receivers.append(edge_receiver)

        for i in range(TOTAL_NUMBER_OF_PRODUCER_CLIENTS):
            connected_edge_receiver = random.choice(edge_receivers)
            transmission = connected_edge_receiver.get_incoming_transmission()
            data_producer = DataProducer(simpy_env=env, results_container=results_container, name=f'DataProducer{i}', transmission_to_data_collector=transmission)
            data_producer.start_producing_data()
    elif config["type"] == "cloud":  # If cloud, setup the cloud and data_producers
        cloud = CloudReceiverAndAggregator(simpy_env=env, results_container=results_container, name='Cloud', mean_distance_km=config['mean_distance_receiver_cloud'], std_distance_km=config['std_distance_receiver_cloud'])
        cloud.start_listening_for_incoming_data()

        for i in range(TOTAL_NUMBER_OF_PRODUCER_CLIENTS):
            transmission = cloud.get_incoming_transmission()
            data_producer = DataProducer(simpy_env=env, results_container=results_container, name=f'DataProducer{i}', transmission_to_data_collector=transmission)
            data_producer.start_producing_data()
    else:
        raise Exception('Type not recognized')

    # Run simulation.
    env.run(until=SIMULATION_DURATION)

    results_container.print_results()
    return results_container


pool = multiprocessing.Pool()
results = pool.map(run_configuration, CONFIGURATIONS)
