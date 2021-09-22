import random

import simpy

from data_producer import DataProducer
from edge_aggregator import EdgeAggregator
from edge_receiver import EdgeReceiver

# Parameters of the edge locations, assuming to have available the Cloudflare network.
# The Cloudflare network at the end of 2021 reports that it has:
# 250 locations,
# 100 Tbps of global network capacity,
# 50 ms put_with_latency from 95% of the world’s Internet-connected population

# Traditional databases and stateful infrastructure usually require you to think about geographical "regions",
# so that you can be sure to store data close to where it is used.
# Thinking about regions can often be an unnatural burden, especially for applications that are not inherently geographical.
from utils import Utils

'''
When a device's user permforms a search, the device sends this information so that it can be preprocessed by a machine learning model and then used to create a list of trending argument per area.

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
Computation perfomed locally + geographical aggregation

Then it can become:
- Only geographical aggregation
- Only computation perfomed locally (ex: publishing videos on social network to avoid modded client)
'''

SIMULATION_DURATION = 2*60*100000  # In milliseconds.
RANDOM_SEED = 42
TOTAL_NUMBER_OF_EDGE_RECEIVERS = 1
TOTAL_NUMBER_OF_EDGE_AGGREGATORS = 2
TOTAL_NUMBER_OF_PRODUCER_CLIENTS = 10


# Setup the simulation.
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Setup processes in the simulation.
edge_aggregators = []
for i in range(TOTAL_NUMBER_OF_EDGE_AGGREGATORS):
    edge_aggregator = EdgeAggregator(simpy_env=env, name=f'EdgeAggregator{i}')
    edge_aggregator.start_listening_for_incoming_data()
    edge_aggregators.append(edge_aggregator)

edge_receivers = []
for i in range(TOTAL_NUMBER_OF_EDGE_RECEIVERS):
    connected_edge_aggregator = random.choice(edge_aggregators)
    transmission = connected_edge_aggregator.get_incoming_transmission()
    edge_receiver = EdgeReceiver(simpy_env=env, name=f'EdgeReceiver{i}', transmission_to_aggregator=transmission)
    edge_receiver.start_listening_for_incoming_data()
    edge_receivers.append(edge_receiver)

data_producers = []
for i in range(TOTAL_NUMBER_OF_PRODUCER_CLIENTS):
    connected_edge_receiver = random.choice(edge_receivers)
    transmission = connected_edge_receiver.get_incoming_transmission()
    data_producer = DataProducer(simpy_env=env, name=f'DataProducer{i}', transmission_to_data_collector=transmission)
    data_producer.start_producing_data()

# Run simulation.
env.run(until=SIMULATION_DURATION)

print("Finished simulation.")
print(f"Created packages: {Utils.total_number_of_data_packages_produced}, processed packages {Utils.total_number_of_data_packages_processed}")
