from typing import Any, Tuple

import simpy

from processing_unit import ProcessingUnit
from results_container import ResultsContainer
from transmission import Transmission
from utils import Utils

EDGE_RECEIVER_CAPACITY = 2  # Number of processes an edge receiver can handle simultaneously (number of cores).
EDGE_RECEIVER_BANDWIDTH_CAPABILITY = 10/1000  # MB that an edge receiver core can process in a millisecond.


class EdgeReceiver(ProcessingUnit):

    def __init__(self, simpy_env: simpy.Environment, results_container: ResultsContainer, name: str, mean_distance_km: float, std_distance_km: float, transmission_to_aggregator: Transmission):
        super().__init__(
            simpy_env=simpy_env,
            results_container=results_container,
            name=name,
            number_of_cores=EDGE_RECEIVER_CAPACITY,
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,
            has_weak_network_initial_delay=True
        )
        self.transmission_to_aggregator = transmission_to_aggregator

    def get_processing_time(self, incoming_message: Any):
        megabytes_of_data_with_creation_time: Tuple[float, simpy.core.SimTime] = incoming_message
        megabytes_of_data = megabytes_of_data_with_creation_time[0]
        time_to_process = megabytes_of_data / EDGE_RECEIVER_BANDWIDTH_CAPABILITY

        data_creation_timestamp = megabytes_of_data_with_creation_time[1]
        first_link_latency = self.simpy_env.now - data_creation_timestamp
        self.results_container.data_packages_passing_first_link += 1
        self.results_container.total_latency_first_link += first_link_latency

        self.results_container.data_packages_processed += 1
        self.results_container.total_latency_processing += time_to_process

        return time_to_process

    def on_processing_ended(self, incoming_message: Any):
        megabytes_of_data_with_creation_time: Tuple[float, simpy.core.SimTime] = incoming_message

        processed_data_size = Utils.get_random_positive_gaussian_value(mean=0.010, std=0.001)
        data_creation_timestamp = megabytes_of_data_with_creation_time[1]
        message = (processed_data_size, data_creation_timestamp)
        self.transmission_to_aggregator.put_in_cable(message)
