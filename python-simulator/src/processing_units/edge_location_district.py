from typing import List

import simpy

from src import architecture_parameters
from src.communication.transmission import Transmission
from src.processing_units.edge_location import EdgeLocation
from src.processing_units.on_processing_ended_enum import OnProcessingEndedEnum
from src.result_container import ResultContainer


class EdgeLocationDistrict(EdgeLocation):
    def __init__(
            self,
            simpy_env: simpy.Environment,
            result_container: ResultContainer,
            name: str,

            mean_distance_km: float,
            std_distance_km: float,

            on_processing_ended_specification: OnProcessingEndedEnum,
            transmissions_to_aggregators: List[Transmission] = None,
    ):
        super().__init__(
            simpy_env=simpy_env,
            result_container=result_container,
            name=name,

            number_of_cores=architecture_parameters.NUMBER_OF_CORES_DISTRICT,
            bandwidth_capability=architecture_parameters.BANDWIDTH_CAPABILITY_DISTRICT,
            mean_processing_start_delay=architecture_parameters.MEAN_PROCESSING_START_DELAY_DISTRICT,
            std_processing_start_delay=architecture_parameters.STD_PROCESSING_START_DELAY_DISTRICT,

            is_data_coming_from_first_link=True,  # For district is always coming from first link.
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,

            on_processing_ended_specification=on_processing_ended_specification,
            transmissions_to_aggregators=transmissions_to_aggregators,
        )
