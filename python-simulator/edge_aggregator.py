import simpy

from transmission import Transmission
from utils import Utils

EDGE_AGGREGATOR_CAPACITY = 8  # Number of processes an edge aggregator can handle simultaneously (number of cores).
EDGE_AGGREGATOR_BANDWIDTH_CAPABILITY = 2/1000  # MB that an edge aggregator core can process in a millisecond.


class EdgeAggregator(object):
    def __init__(self, simpy_env: simpy.Environment, name: str):
        self.simpy_env = simpy_env
        self.name = name
        self.transmission_from_edge_receiver = Transmission(simpy_env=simpy_env, mean_distance_km=3000.0, std_distance_km=1000.0, is_weak_network=False)
        self.cores_resource = simpy.Resource(simpy_env, capacity=EDGE_AGGREGATOR_CAPACITY)

    def get_transmission_from_edge_receiver(self) -> Transmission:
        return self.transmission_from_edge_receiver

    def start_listening_for_data(self):
        self.simpy_env.process(self.data_receiver())

    def data_receiver(self):
        while True:
            if Utils.PRINT_TIME_MESSAGES:
                print(f'{self.name} waiting from data')
            megabytes_of_data = yield self.transmission_from_edge_receiver.get_from_cable()
            arrive_time = self.simpy_env.now
            if Utils.PRINT_TIME_MESSAGES:
                print(f'{self.name} received {megabytes_of_data} MB of data at {arrive_time}')

            self.simpy_env.process(self.edge_aggregator_processing(megabytes_of_data=megabytes_of_data, arrive_time=arrive_time))

    def edge_aggregator_processing(self, megabytes_of_data: float, arrive_time: simpy.core.SimTime):
        with self.cores_resource.request() as req:
            yield req
            ready_time = self.simpy_env.now
            if (ready_time - arrive_time) > 0.0:
                print(f'Cores where not free, waiting time: {ready_time - arrive_time}')

            time_to_process = megabytes_of_data / EDGE_AGGREGATOR_BANDWIDTH_CAPABILITY
            yield self.simpy_env.timeout(time_to_process)
            processed_time = self.simpy_env.now
            if Utils.PRINT_TIME_MESSAGES:
                print(f"{self.name} processed at {processed_time}, processing time: {processed_time - ready_time}")
