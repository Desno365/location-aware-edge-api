from typing import Any

import simpy

from processing_unit import ProcessingUnit


EDGE_AGGREGATOR_CAPACITY = 8  # Number of processes an edge aggregator can handle simultaneously (number of cores).
EDGE_AGGREGATOR_BANDWIDTH_CAPABILITY = 2/1000  # MB that an edge aggregator core can process in a millisecond.


class EdgeAggregator(ProcessingUnit):
    def __init__(self, simpy_env: simpy.Environment, name: str):
        super().__init__(
            simpy_env=simpy_env,
            name=name,
            number_of_cores=EDGE_AGGREGATOR_CAPACITY,
            mean_distance_km=3000.0,
            std_distance_km=1000.0,
            is_weak_network=False
        )

    def get_processing_time(self, incoming_message: Any):
        megabytes_of_data: float = incoming_message
        return megabytes_of_data / EDGE_AGGREGATOR_BANDWIDTH_CAPABILITY

    def on_processing_ended(self, incoming_message: Any):
        pass
