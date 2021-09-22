import abc
from typing import Any

import simpy

from transmission import Transmission
from utils import Utils


class ProcessingUnit(metaclass=abc.ABCMeta):

    def __init__(self, simpy_env: simpy.Environment, name: str, number_of_cores: int, mean_distance_km: float, std_distance_km: float, is_weak_network: bool):
        assert simpy_env is not None
        assert name is not None
        assert number_of_cores > 0
        assert mean_distance_km > 0.0
        assert std_distance_km > 0.0
        assert is_weak_network is True or is_weak_network is False

        self.simpy_env = simpy_env
        self.name = name
        self.cores_resource = simpy.Resource(env=simpy_env, capacity=number_of_cores)
        self.incoming_transmission = Transmission(
            simpy_env=simpy_env,
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,
            is_weak_network=is_weak_network
        )

    def get_incoming_transmission(self) -> Transmission:
        return self.incoming_transmission

    def start_listening_for_incoming_data(self):
        self.simpy_env.process(self.data_receiver_process())

    def data_receiver_process(self):
        while True:
            if Utils.PRINT_TIME_MESSAGES:
                print(f'{self.name} waiting for data')
            message = yield self.incoming_transmission.get_from_cable()
            arrive_time = self.simpy_env.now
            if Utils.PRINT_TIME_MESSAGES:
                print(f'{self.name} received message {message} at {arrive_time}')

            self.simpy_env.process(self.single_core_process(incoming_message=message, arrive_time=arrive_time))

    def single_core_process(self, incoming_message: Any, arrive_time: simpy.core.SimTime):
        with self.cores_resource.request() as req:
            yield req
            ready_time = self.simpy_env.now
            if (ready_time - arrive_time) > 0.0:
                print(f'Cores in {self.name} where not free, waiting time: {ready_time - arrive_time}')

            time_to_process = self.get_processing_time(incoming_message=incoming_message)
            yield self.simpy_env.timeout(time_to_process)
            processed_time = self.simpy_env.now
            if Utils.PRINT_TIME_MESSAGES:
                print(f"{self.name} processed at {processed_time}, processing time: {processed_time - ready_time}")

            self.on_processing_ended(incoming_message=incoming_message)

    @abc.abstractmethod
    def get_processing_time(self, incoming_message: Any):
        pass

    @abc.abstractmethod
    def on_processing_ended(self, incoming_message: Any):
        pass
