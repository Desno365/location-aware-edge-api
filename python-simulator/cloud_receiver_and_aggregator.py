from typing import Any, Tuple

import simpy

from processing_unit import ProcessingUnit
from results_container import ResultsContainer

CLOUD_CAPACITY = 1000  # Number of processes the cloud can handle simultaneously (number of cores).
CLOUD_BANDWIDTH_CAPABILITY = 20/1000  # MB that a cloud core can process in a millisecond.


class CloudReceiverAndAggregator(ProcessingUnit):
    def __init__(self, simpy_env: simpy.Environment, results_container: ResultsContainer, name: str, mean_distance_km: float, std_distance_km: float):
        super().__init__(
            simpy_env=simpy_env,
            results_container=results_container,
            name=name,
            number_of_cores=CLOUD_CAPACITY,
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,
            has_weak_network_initial_delay=True
        )

    def get_processing_time(self, incoming_message: Any):
        megabytes_of_data_with_creation_time: Tuple[float, simpy.core.SimTime] = incoming_message
        megabytes_of_data = megabytes_of_data_with_creation_time[0]
        time_to_process = megabytes_of_data / CLOUD_BANDWIDTH_CAPABILITY

        data_creation_timestamp = megabytes_of_data_with_creation_time[1]
        first_link_latency = self.simpy_env.now - data_creation_timestamp
        self.results_container.data_packages_passing_first_link += 1
        self.results_container.total_latency_first_link += first_link_latency

        self.results_container.data_packages_processed += 1
        self.results_container.total_latency_processing += time_to_process

        return time_to_process

    def on_processing_ended(self, incoming_message: Any):
        megabytes_of_data_with_creation_time: Tuple[float, simpy.core.SimTime] = incoming_message
        data_creation_timestamp = megabytes_of_data_with_creation_time[1]
        latency = self.simpy_env.now - data_creation_timestamp

        self.results_container.data_packages_aggregated += 1
        self.results_container.total_latency_from_creation_to_aggregation += latency
