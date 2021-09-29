import simpy

from src.processing_units.processing_unit import ProcessingUnit
from src.result_container import ResultContainer
from src.transmission import DataMessageType
from src.utils import Utils

CLOUD_CAPACITY = 1000  # Number of processes the cloud can handle simultaneously (number of cores).
CLOUD_BANDWIDTH_CAPABILITY = 20/1000  # MB that a cloud core can process in a millisecond.

MEAN_PROCESSING_START_DELAY = 4.0
STD_PROCESSING_START_DELAY = 1.0


class CloudReceiverAndAggregator(ProcessingUnit):
    def __init__(self, simpy_env: simpy.Environment, result_container: ResultContainer, name: str, mean_distance_km: float, std_distance_km: float):
        super().__init__(
            simpy_env=simpy_env,
            result_container=result_container,
            name=name,
            number_of_cores=CLOUD_CAPACITY,
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,
            has_weak_network_initial_delay=True
        )

    def on_data_message_received(self, incoming_message: DataMessageType) -> None:
        data_sent_timestamp = incoming_message[2]
        first_link_latency = self.simpy_env.now - data_sent_timestamp
        self.result_container.data_packages_passing_first_link += 1
        self.result_container.total_latency_first_link += first_link_latency

    def get_processing_time(self, incoming_message: DataMessageType) -> float:
        megabytes_of_data = incoming_message[0]
        start_delay = Utils.get_random_positive_gaussian_value(mean=MEAN_PROCESSING_START_DELAY, std=STD_PROCESSING_START_DELAY)
        time_to_process = start_delay + (megabytes_of_data / CLOUD_BANDWIDTH_CAPABILITY)

        return time_to_process

    def on_processing_ended(self, incoming_message: DataMessageType, total_processing_time: float) -> None:
        # Add processing time to results.
        self.result_container.data_packages_passing_first_processing += 1
        self.result_container.total_latency_first_processing += total_processing_time

        # Add start-to-finish time to results.
        data_creation_timestamp = incoming_message[1]
        total_latency = self.simpy_env.now - data_creation_timestamp
        self.result_container.data_packages_aggregated += 1
        self.result_container.total_latency_from_creation_to_aggregation += total_latency
