import simpy

from src.communication.data_message import DataMessage
from src.processing_units.processing_unit import ProcessingUnit
from src.result_container import ResultContainer
from src.communication.transmission import Transmission
from src.utils import Utils

EDGE_RECEIVER_CAPACITY = 2  # Number of processes an edge receiver can handle simultaneously (number of cores).
EDGE_RECEIVER_BANDWIDTH_CAPABILITY = 10/1000  # MB that an edge receiver core can process in a millisecond.

MEAN_SIZE_FOR_PROCESSED_DATA = 0.010  # In MB.
STD_SIZE_FOR_PROCESSED_DATA = 0.001  # In MB.

MEAN_PROCESSING_START_DELAY = 4.0
STD_PROCESSING_START_DELAY = 1.0


class EdgeReceiver(ProcessingUnit):

    def __init__(self, simpy_env: simpy.Environment, result_container: ResultContainer, name: str, mean_distance_km: float, std_distance_km: float, transmission_to_aggregator: Transmission):
        super().__init__(
            simpy_env=simpy_env,
            result_container=result_container,
            name=name,
            number_of_cores=EDGE_RECEIVER_CAPACITY,
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,
            has_weak_network_initial_delay=True
        )
        self.transmission_to_aggregator = transmission_to_aggregator

    def on_data_message_received(self, incoming_message: DataMessage) -> None:
        self.result_container.data_packages_passing_first_link += 1
        self.result_container.total_latency_first_link += incoming_message.latency_acquired
        self.result_container.traffic_per_distance_first_link += (incoming_message.megabytes_of_data * incoming_message.distance_traveled)

    def get_processing_time(self, incoming_message: DataMessage) -> float:
        megabytes_of_data = incoming_message.megabytes_of_data
        start_delay = Utils.get_random_positive_gaussian_value(mean=MEAN_PROCESSING_START_DELAY, std=STD_PROCESSING_START_DELAY)
        time_to_process = start_delay + (megabytes_of_data / EDGE_RECEIVER_BANDWIDTH_CAPABILITY)

        return time_to_process

    def on_processing_ended(self, incoming_message: DataMessage, total_processing_time: float) -> None:
        # Add processing time to results.
        self.result_container.data_packages_passing_first_processing += 1
        self.result_container.total_latency_first_processing += total_processing_time

        # Send processed message to aggregator.
        processed_data_size = Utils.get_random_positive_gaussian_value(mean=MEAN_SIZE_FOR_PROCESSED_DATA, std=STD_SIZE_FOR_PROCESSED_DATA)
        message = DataMessage(
            megabytes_of_data=processed_data_size,
            original_data_creation_time=incoming_message.original_data_creation_time,
            data_sent_time=self.simpy_env.now
        )
        self.transmission_to_aggregator.put_in_cable(message)
