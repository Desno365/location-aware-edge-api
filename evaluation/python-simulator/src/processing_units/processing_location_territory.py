from typing import List

import simpy

from src import default_architecture_parameters
from src.communication.transmission import Transmission
from src.processing_units.processing_location import ProcessingLocation
from src.processing_units.on_processing_ended_enum import OnProcessingEndedEnum
from src.result_container import ResultContainer


class ProcessingLocationTerritory(ProcessingLocation):
    def __init__(
            self,
            simpy_env: simpy.Environment,
            result_container: ResultContainer,
            name: str,

            is_data_coming_from_first_link: bool,  # True if coming from first link, False if coming from second link.
            mean_distance_km: float,
            std_distance_km: float,

            on_processing_ended_specification: OnProcessingEndedEnum,
            transmissions_to_aggregators: List[Transmission] = None,
    ):
        super().__init__(
            simpy_env=simpy_env,
            result_container=result_container,
            name=name,

            number_of_cores=default_architecture_parameters.NUMBER_OF_CORES_TERRITORY,
            bandwidth_capability=default_architecture_parameters.BANDWIDTH_CAPABILITY_TERRITORY,
            mean_processing_start_delay=default_architecture_parameters.MEAN_PROCESSING_START_DELAY_TERRITORY,
            std_processing_start_delay=default_architecture_parameters.STD_PROCESSING_START_DELAY_TERRITORY,

            is_data_coming_from_first_link=is_data_coming_from_first_link,
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,

            on_processing_ended_specification=on_processing_ended_specification,
            transmissions_to_aggregators=transmissions_to_aggregators,
        )
