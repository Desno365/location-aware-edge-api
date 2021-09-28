from typing import Any, Tuple

import simpy

from processing_unit import ProcessingUnit
from results_container import ResultsContainer

EDGE_AGGREGATOR_CAPACITY = 8  # Number of processes an edge aggregator can handle simultaneously (number of cores).
EDGE_AGGREGATOR_BANDWIDTH_CAPABILITY = 15/1000  # MB that an edge aggregator core can process in a millisecond.


class EdgeAggregator(ProcessingUnit):
    def __init__(self, simpy_env: simpy.Environment, results_container: ResultsContainer, name: str, mean_distance_km: float, std_distance_km: float):
        super().__init__(
            simpy_env=simpy_env,
            results_container=results_container,
            name=name,
            number_of_cores=EDGE_AGGREGATOR_CAPACITY,
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,
            has_weak_network_initial_delay=False
        )

    def get_processing_time(self, incoming_message: Any):
        megabytes_of_data_with_creation_time: Tuple[float, simpy.core.SimTime] = incoming_message
        megabytes_of_data = megabytes_of_data_with_creation_time[0]
        return megabytes_of_data / EDGE_AGGREGATOR_BANDWIDTH_CAPABILITY

    def on_processing_ended(self, incoming_message: Any):
        megabytes_of_data_with_creation_time: Tuple[float, simpy.core.SimTime] = incoming_message
        data_creation_timestamp = megabytes_of_data_with_creation_time[1]
        latency = self.simpy_env.now - data_creation_timestamp

        self.results_container.data_packages_aggregated += 1
        self.results_container.total_latency_from_creation_to_aggregation += latency
