import random
from typing import List

import simpy

from result_container import ResultContainer
from src.communication.data_message import DataMessage
from src.communication.transmission import Transmission
from utils import Utils

MEAN_TIME_FOR_NEW_DATA_READ = 5000.0  # In milliseconds.
STD_TIME_FOR_NEW_DATA_READ = 2000.0  # In milliseconds.

MEAN_SIZE_FOR_NEW_DATA_READ_REQUEST = 0.010  # In MB.
STD_SIZE_FOR_NEW_DATA_READ_REQUEST = 0.001  # In MB.


class DataReader(object):

    def __init__(
            self,
            simpy_env: simpy.Environment,
            result_container: ResultContainer,
            name: str,
            probabilities: List[float],
            transmission_to_location: Transmission,
            transmission_to_city: Transmission,
            transmission_to_territory: Transmission,
            transmission_to_country: Transmission,
            transmission_to_continent: Transmission,
            transmission_to_central: Transmission,
    ):
        assert len(probabilities) == 6
        self.simpy_env = simpy_env
        self.result_container = result_container
        self.name = name
        self.probabilities = probabilities
        self.transmission_to_location = transmission_to_location
        self.transmission_to_city = transmission_to_city
        self.transmission_to_territory = transmission_to_territory
        self.transmission_to_country = transmission_to_country
        self.transmission_to_continent = transmission_to_continent
        self.transmission_to_central = transmission_to_central

    def start_reading_data(self):
        self.simpy_env.process(self.data_producer_process())

    def data_producer_process(self):
        """A process which randomly generates messages."""
        while True:
            # Wait a random time for the next data read.
            time_to_wait_for_next_data = Utils.get_random_positive_gaussian_value(mean=MEAN_TIME_FOR_NEW_DATA_READ, std=STD_TIME_FOR_NEW_DATA_READ)
            yield self.simpy_env.timeout(time_to_wait_for_next_data)
            
            # Chose level to send.
            extraction = random.uniform(0.0, 1.0)
            if extraction - (self.probabilities[0]) <= 0.0:
                transmission = self.transmission_to_location
            elif extraction - (self.probabilities[0] + self.probabilities[1]) <= 0.0:
                transmission = self.transmission_to_city
            elif extraction - (self.probabilities[0] + self.probabilities[1] + self.probabilities[2]) <= 0.0:
                transmission = self.transmission_to_territory
            elif extraction - (self.probabilities[0] + self.probabilities[1] + self.probabilities[2] + self.probabilities[3]) <= 0.0:
                transmission = self.transmission_to_country
            elif extraction - (self.probabilities[0] + self.probabilities[1] + self.probabilities[2] + self.probabilities[3] + self.probabilities[4]) <= 0.0:
                transmission = self.transmission_to_continent
            elif extraction - (self.probabilities[0] + self.probabilities[1] + self.probabilities[2] + self.probabilities[3] + self.probabilities[4] + self.probabilities[5]) <= 0.0:
                transmission = self.transmission_to_central

            # Send random data size.
            created_data_size = Utils.get_random_positive_gaussian_value(mean=MEAN_SIZE_FOR_NEW_DATA_READ_REQUEST, std=STD_SIZE_FOR_NEW_DATA_READ_REQUEST)
            message = DataMessage(megabytes_of_data=created_data_size, original_data_creation_time=self.simpy_env.now, data_sent_time=self.simpy_env.now)
            if Utils.PRINT_TIME_MESSAGES:
                print(f'{self.name} has waited {time_to_wait_for_next_data} and now is sending {created_data_size} MB of read request data.')
            transmission.put_in_cable(message)
            self.result_container.data_packages_produced += 1
