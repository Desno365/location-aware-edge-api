import simpy

from src.communication.transmission import Transmission
from src.processing_units.edge_location import EdgeLocation
from src.result_container import ResultContainer

NUMBER_OF_CORES = 2
BANDWIDTH_CAPABILITY = 10/1000  # MB that a core can process in a millisecond.

MEAN_PROCESSING_START_DELAY = 5.0
STD_PROCESSING_START_DELAY = 2.0


class EdgeLocationDistrict(EdgeLocation):
    def __init__(
            self,
            simpy_env: simpy.Environment,
            result_container: ResultContainer,
            name: str,

            mean_distance_km: float,
            std_distance_km: float,

            should_send_processed_data_to_aggregator: bool,
            transmission_to_aggregator: Transmission = None,
    ):
        super().__init__(
            simpy_env=simpy_env,
            result_container=result_container,
            name=name,

            number_of_cores=NUMBER_OF_CORES,
            bandwidth_capability=BANDWIDTH_CAPABILITY,
            mean_processing_start_delay=MEAN_PROCESSING_START_DELAY,
            std_processing_start_delay=STD_PROCESSING_START_DELAY,

            is_data_coming_from_first_link=True,  # For district is always coming from first link.
            mean_distance_km=mean_distance_km,
            std_distance_km=std_distance_km,

            should_send_processed_data_to_aggregator=should_send_processed_data_to_aggregator,
            transmission_to_aggregator=transmission_to_aggregator,
        )
