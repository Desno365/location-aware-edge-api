import simpy

from src import architecture_parameters
from src.communication.transmission import Transmission
from src.processing_units.edge_location import EdgeLocation
from src.result_container import ResultContainer


class EdgeLocationContinent(EdgeLocation):
    def __init__(
            self,
            simpy_env: simpy.Environment,
            result_container: ResultContainer,
            name: str,

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

            number_of_cores=architecture_parameters.NUMBER_OF_CORES_CONTINENT,
            bandwidth_capability=architecture_parameters.BANDWIDTH_CAPABILITY_CONTINENT,
            mean_processing_start_delay=architecture_parameters.MEAN_PROCESSING_START_DELAY_CONTINENT,
            std_processing_start_delay=architecture_parameters.STD_PROCESSING_START_DELAY_CONTINENT,

            is_data_coming_from_first_link=is_data_coming_from_first_link,
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,

            should_send_processed_data_to_aggregator=should_send_processed_data_to_aggregator,
            transmission_to_aggregator=transmission_to_aggregator,
        )
