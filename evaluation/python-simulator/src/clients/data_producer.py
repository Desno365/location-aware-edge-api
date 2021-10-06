import simpy

from src.communication.data_message import DataMessage
from src.communication.transmission import Transmission
from src.result_container import ResultContainer
from src.utils import Utils

MEAN_TIME_FOR_NEW_DATA_PRODUCED = 10000.0  # In milliseconds.
STD_TIME_FOR_NEW_DATA_PRODUCED = 3000.0  # In milliseconds.

MEAN_SIZE_FOR_NEW_DATA_PRODUCED = 0.423  # In MB. Average Full HD JPG 100% quality: 423.41 KB. For average size used this tool https://toolstud.io/photo/megapixel.php
STD_SIZE_FOR_NEW_DATA_PRODUCED = 0.150  # In MB.


class DataProducer(object):

    def __init__(self, simpy_env: simpy.Environment, result_container: ResultContainer, name: str, transmission_to_data_collector: Transmission, number_of_packages_to_produce: int or None):
        self.simpy_env = simpy_env
        self.result_container = result_container
        self.name = name
        self.transmission_to_data_collector = transmission_to_data_collector
        self.number_of_packages_to_produce = number_of_packages_to_produce

    def start_producing_data(self):
        self.simpy_env.process(self.data_producer_process())

    def data_producer_process(self):
        """A process which randomly generates messages."""
        number_of_packages_produced = 0
        while self.number_of_packages_to_produce is None or number_of_packages_produced < self.number_of_packages_to_produce:
            # Wait a random time for the next data creation.
            time_to_wait_for_next_data = Utils.get_random_positive_gaussian_value(mean=MEAN_TIME_FOR_NEW_DATA_PRODUCED, std=STD_TIME_FOR_NEW_DATA_PRODUCED,)
            yield self.simpy_env.timeout(time_to_wait_for_next_data)

            # Send random data size.
            created_data_size = Utils.get_random_positive_gaussian_value(mean=MEAN_SIZE_FOR_NEW_DATA_PRODUCED, std=STD_SIZE_FOR_NEW_DATA_PRODUCED)
            message = DataMessage(megabytes_of_data=created_data_size, original_data_creation_time=self.simpy_env.now, data_sent_time=self.simpy_env.now)
            if Utils.PRINT_TIME_MESSAGES:
                print(f'{self.name} has waited {time_to_wait_for_next_data} and now is sending {created_data_size} MB of data.')
            self.transmission_to_data_collector.put_in_cable(message)
            self.result_container.data_packages_produced += 1

            number_of_packages_produced += 1
