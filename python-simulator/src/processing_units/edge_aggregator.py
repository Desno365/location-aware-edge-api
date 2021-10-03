import simpy

from src.communication.data_message import DataMessage
from src.processing_units.processing_unit import ProcessingUnit
from src.result_container import ResultContainer
from src.utils import Utils

EDGE_AGGREGATOR_CAPACITY = 8  # Number of processes an edge aggregator can handle simultaneously (number of cores).
EDGE_AGGREGATOR_BANDWIDTH_CAPABILITY = 15/1000  # MB that an edge aggregator core can process in a millisecond.

MEAN_PROCESSING_START_DELAY = 4.0
STD_PROCESSING_START_DELAY = 1.0


class EdgeAggregator(ProcessingUnit):
    def __init__(self, simpy_env: simpy.Environment, result_container: ResultContainer, name: str, mean_distance_km: float, std_distance_km: float):
        super().__init__(
            simpy_env=simpy_env,
            result_container=result_container,
            name=name,
            number_of_cores=EDGE_AGGREGATOR_CAPACITY,
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,
            has_weak_network_initial_delay=False
        )

    def on_data_message_received(self, incoming_message: DataMessage) -> None:
        self.result_container.report_second_link_latency_traffic_and_distance(
            latency=incoming_message.latency_acquired,
            traffic=incoming_message.megabytes_of_data,
            distance=incoming_message.distance_traveled,
        )

    def get_processing_time(self, incoming_message: DataMessage) -> float:
        megabytes_of_data = incoming_message.megabytes_of_data
        start_delay = Utils.get_random_positive_gaussian_value(mean=MEAN_PROCESSING_START_DELAY, std=STD_PROCESSING_START_DELAY)
        time_to_process = start_delay + (megabytes_of_data / EDGE_AGGREGATOR_BANDWIDTH_CAPABILITY)

        return time_to_process

    def on_processing_ended(self, incoming_message: DataMessage, total_processing_time: float) -> None:
        # Add processing time to results.
        self.result_container.report_second_processing_latency(latency=total_processing_time)

        # Add start-to-finish time to results.
        total_latency = self.simpy_env.now - incoming_message.original_data_creation_time
        self.result_container.report_total_finished_latency(latency=total_latency)
