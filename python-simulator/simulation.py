# Parameters of the edge locations, assuming to have available the Cloudflare network.
# The Cloudflare network at the end of 2021 reports that it has:
# 250 locations,
# 100 Tbps of global network capacity,
# 50 ms put_with_latency from 95% of the world’s Internet-connected population

# Traditional databases and stateful infrastructure usually require you to think about geographical "regions",
# so that you can be sure to store data close to where it is used.
# Thinking about regions can often be an unnatural burden, especially for applications that are not inherently geographical.

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

from edge_receiver import EdgeReceiver
from transmission import Transmission
from utils import Utils

'''
General use case:
Computation perfomed locally + geographical aggregation

Then it can become:
- Only geographical aggregation
- Only computation perfomed locally (ex: publishing videos on social network to avoid modded client)
'''

import random
import simpy


# Backbone = average of inter-region latencies between us-east-1 and other AWS regions: https://docs.aviatrix.com/_images/inter_region_latency.png
# + 30 to reach clients from backbone
def get_latency_cloud_from_client_to_central():
    return get_value_from_normal_distribution_with_max_or_min(mean=115.0 + 30.0, std=20.0 + 10.0, min_value=1.0)


# Size in MB of the data produced.
def get_data_produced_size():
    return get_value_from_normal_distribution_with_max_or_min(mean=1.0, std=0.33, min_value=0.1)


def get_value_from_normal_distribution_with_max_or_min(mean: float, std: float, min_value: float = None, max_value: float = None):
    value = None
    while value is None or (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
        value = random.gauss(mean, std)
    return value


SIMULATION_DURATION = 2*60*1000  # In milliseconds.
RANDOM_SEED = 42
TOTAL_NUMBER_OF_EDGE_RECEIVERS = 1
TOTAL_NUMBER_OF_PRODUCER_CLIENTS = 10
MEAN_TIME_FOR_NEW_DATA_PRODUCED = 10000.0  # In milliseconds.
STD_TIME_FOR_NEW_DATA_PRODUCED = 3000.0  # In milliseconds.


def data_producer(simpy_env: simpy.Environment, name: str, transmission_to_edge: Transmission):
    """A process which randomly generates messages."""
    while True:
        # Wait a random time for the next data creation.
        time_to_wait_for_next_data = Utils.get_random_positive_gaussian_value(
            mean=MEAN_TIME_FOR_NEW_DATA_PRODUCED,
            std=STD_TIME_FOR_NEW_DATA_PRODUCED,
        )
        yield simpy_env.timeout(time_to_wait_for_next_data)

        # Send random data size.
        data_produced = get_data_produced_size()
        if Utils.PRINT_TIME_MESSAGES:
            print(f'{name} has waited {time_to_wait_for_next_data} and now is sending {data_produced} MB of data.')
        transmission_to_edge.put_in_cable(data_produced)


# Setup the simulation.
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Setup processes in the simulation.
edge_receivers = []
for i in range(TOTAL_NUMBER_OF_EDGE_RECEIVERS):
    edge_receiver = EdgeReceiver(simpy_env=env, name=f'EdgeReceiver{i}')
    edge_receiver.start_listening_for_data()
    edge_receivers.append(edge_receiver)

for i in range(TOTAL_NUMBER_OF_PRODUCER_CLIENTS):
    connected_edge_receiver = random.choice(edge_receivers)
    transmission = connected_edge_receiver.get_transmission_from_client()
    env.process(data_producer(simpy_env=env, name=f'DataProducer{i}', transmission_to_edge=transmission))

# Run simulation.
env.run(until=SIMULATION_DURATION)
