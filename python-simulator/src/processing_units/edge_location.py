import simpy

from src.communication.data_message import DataMessage
from src.communication.transmission import Transmission
from src.processing_units.processing_unit import ProcessingUnit
from src.result_container import ResultContainer
from src.utils import Utils

MEAN_SIZE_FOR_PROCESSED_DATA = 0.010  # In MB.
STD_SIZE_FOR_PROCESSED_DATA = 0.001  # In MB.


class EdgeLocation(ProcessingUnit):
    def __init__(
            self,
            simpy_env: simpy.Environment,
            result_container: ResultContainer,
            name: str,

            number_of_cores: int,  # Number of processes an edge location can handle simultaneously (number of cores).
            bandwidth_capability: float,  # MB that an edge aggregator core can process in a millisecond.
            mean_processing_start_delay: float,
            std_processing_start_delay: float,

            is_data_coming_from_first_link: bool,  # True if coming from first link, False if coming from second link.
            mean_distance_km: float,
            std_distance_km: float,

            should_send_processed_data_to_aggregator: bool,
            transmission_to_aggregator: Transmission = None,
    ):
        super().__init__(
            simpy_env=simpy_env,
            result_container=result_container,
            name=name,
            number_of_cores=number_of_cores,
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,
            has_weak_network_initial_delay=is_data_coming_from_first_link  # The first link (user-to-location) must traverse a weak network initially.
        )
        assert bandwidth_capability > 0.0
        assert mean_processing_start_delay >= 0.0
        assert std_processing_start_delay >= 0.0
        assert not should_send_processed_data_to_aggregator or transmission_to_aggregator is not None  # If should_send_processed_data_to_aggregator is True then transmission_to_aggregator must be defined.
        self.bandwidth_capability = bandwidth_capability
        self.mean_processing_start_delay = mean_processing_start_delay
        self.std_processing_start_delay = std_processing_start_delay
        self.is_data_coming_from_first_link = is_data_coming_from_first_link
        self.should_send_processed_data_to_aggregator = should_send_processed_data_to_aggregator
        self.transmission_to_aggregator = transmission_to_aggregator

    def on_data_message_received(self, incoming_message: DataMessage) -> None:
        if self.is_data_coming_from_first_link:
            self.result_container.report_first_link_latency_traffic_and_distance(
                latency=incoming_message.latency_acquired,
                traffic=incoming_message.megabytes_of_data,
                distance=incoming_message.distance_traveled,
            )
        else:
            self.result_container.report_second_link_latency_traffic_and_distance(
                latency=incoming_message.latency_acquired,
                traffic=incoming_message.megabytes_of_data,
                distance=incoming_message.distance_traveled,
            )

    def get_processing_time(self, incoming_message: DataMessage) -> float:
        megabytes_of_data = incoming_message.megabytes_of_data
        start_delay = Utils.get_random_positive_gaussian_value(mean=self.mean_processing_start_delay, std=self.std_processing_start_delay)
        time_to_process = start_delay + (megabytes_of_data / self.bandwidth_capability)
        return time_to_process

    def on_processing_ended(self, incoming_message: DataMessage, total_processing_time: float) -> None:
        # Add processing time to results.
        if self.is_data_coming_from_first_link:
            self.result_container.report_first_processing_latency(latency=total_processing_time)
        else:
            self.result_container.report_second_processing_latency(latency=total_processing_time)

        if self.should_send_processed_data_to_aggregator:
            # Send processed message to aggregator.
            processed_data_size = Utils.get_random_positive_gaussian_value(mean=MEAN_SIZE_FOR_PROCESSED_DATA, std=STD_SIZE_FOR_PROCESSED_DATA)
            message = DataMessage(
                megabytes_of_data=processed_data_size,
                original_data_creation_time=incoming_message.original_data_creation_time,
                data_sent_time=self.simpy_env.now
            )
            self.transmission_to_aggregator.put_in_cable(message)
        else:
            # Add start-to-finish time to results.
            total_latency = self.simpy_env.now - incoming_message.original_data_creation_time
            self.result_container.report_total_finished_latency(latency=total_latency)
