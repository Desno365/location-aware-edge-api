from typing import Any

import simpy

from processing_unit import ProcessingUnit

EDGE_RECEIVER_CAPACITY = 2  # Number of processes an edge receiver can handle simultaneously (number of cores).
EDGE_RECEIVER_BANDWIDTH_CAPABILITY = 1/1000  # MB that an edge receiver core can process in a millisecond.


class EdgeReceiver(ProcessingUnit):

    def __init__(self, simpy_env: simpy.Environment, name: str):
        super().__init__(
            simpy_env=simpy_env,
            name=name,
            number_of_cores=EDGE_RECEIVER_CAPACITY,
            mean_distance_km=60.0,
            std_distance_km=20.0,
            is_weak_network=True
        )

    def get_processing_time(self, incoming_message: Any):
        megabytes_of_data: float = incoming_message
        return megabytes_of_data / EDGE_RECEIVER_BANDWIDTH_CAPABILITY

    def on_processing_ended(self, incoming_message: Any):
        print("")
