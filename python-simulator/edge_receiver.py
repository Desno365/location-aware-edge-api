import simpy

from transmission import Transmission
from utils import Utils

EDGE_RECEIVER_CAPACITY = 2  # Number of processes an edge receiver can handle simultaneously (number of cores).
EDGE_RECEIVER_BANDWIDTH_CAPABILITY = 1/1000  # MB that an edge receiver core can process in a millisecond.


class EdgeReceiver(object):
    def __init__(self, simpy_env: simpy.Environment, name: str):
        self.simpy_env = simpy_env
        self.name = name
        self.transmission_from_client = Transmission(simpy_env=simpy_env, mean_distance_km=60.0, std_distance_km=20.0, is_weak_network=True)
        self.cores_resource = simpy.Resource(simpy_env, capacity=EDGE_RECEIVER_CAPACITY)

    def get_transmission_from_client(self) -> Transmission:
        return self.transmission_from_client

    def start_listening_for_data(self):
        self.simpy_env.process(self.data_receiver())

    def data_receiver(self):
        while True:
            if Utils.PRINT_TIME_MESSAGES:
                print(f'{self.name} waiting from data')
            megabytes_of_data = yield self.transmission_from_client.get_from_cable()
            arrive_time = self.simpy_env.now
            if Utils.PRINT_TIME_MESSAGES:
                print(f'{self.name} received {megabytes_of_data} MB of data at {arrive_time}')

            self.simpy_env.process(self.edge_processer(megabytes_of_data=megabytes_of_data, arrive_time=arrive_time))

    def edge_processer(self, megabytes_of_data: float, arrive_time: simpy.core.SimTime):
        with self.cores_resource.request() as req:
            yield req
            ready_time = self.simpy_env.now
            if (ready_time - arrive_time) > 0.0:
                print(f'Cores where not free, waiting time: {ready_time - arrive_time}')

            time_to_process = megabytes_of_data / EDGE_RECEIVER_BANDWIDTH_CAPABILITY
            yield self.simpy_env.timeout(time_to_process)
            processed_time = self.simpy_env.now
            if Utils.PRINT_TIME_MESSAGES:
                print(f"{self.name} processed at {processed_time}, processing time: {processed_time - ready_time}")

            time_to_aggregate = get_latency_edge_from_location_to_city()
            yield self.simpy_env.timeout(time_to_aggregate)
            finish_time = self.simpy_env.now
            if Utils.PRINT_TIME_MESSAGES:
                print(f"{self.name} finished at {finish_time}, delta time {finish_time - arrive_time}")


# 50 ms latency from 95% of the world’s Internet-connected population. 95% = 2*std + mean
def get_latency_edge_from_client_to_location():
    return Utils.get_random_positive_gaussian_value(mean=30.0, std=10.0)


# Faster connection than client-location, so also less std.
def get_latency_edge_from_location_to_city():
    return Utils.get_random_positive_gaussian_value(mean=15.0, std=3.3)


# Faster connection than client-location but more spread apart
def get_latency_edge_from_city_to_territory():
    return Utils.get_random_positive_gaussian_value(mean=30.0, std=6.6)


# Faster connection than client-location but a lot more spread apart
def get_latency_edge_from_territory_to_country():
    return Utils.get_random_positive_gaussian_value(mean=40.0, std=8.8)


# Faster connection than client-location but a lot more spread apart
def get_latency_edge_from_country_to_continent():
    return Utils.get_random_positive_gaussian_value(mean=60.0, std=13.2)
