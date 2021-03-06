import math
import statistics


class ResultContainer:

    def __init__(self, simulation_name: str, simulation_type: str):
        self.simulation_name = simulation_name
        self.simulation_type = simulation_type

        self.data_packages_produced = 0

        # Latencies variables.
        self.latency_first_link_list = []
        self.latency_first_processing_list = []
        self.latency_second_link_list = []
        self.latency_second_processing_list = []
        self.latency_total_finished_list = []

        # Traffic variables.
        self.traffic_per_distance_first_link_list = []
        self.traffic_per_distance_second_link_list = []

        # Distance variables.
        self.distance_first_link_list = []
        self.distance_second_link_list = []

    def report_first_link_latency_traffic_and_distance(self, latency: float, traffic: float, distance: float) -> None:
        self.latency_first_link_list.append(latency)
        traffic_per_distance = (traffic * distance)
        self.traffic_per_distance_first_link_list.append(traffic_per_distance)
        self.distance_first_link_list.append(distance)

    def report_first_processing_latency(self, latency: float) -> None:
        self.latency_first_processing_list.append(latency)

    def report_second_link_latency_traffic_and_distance(self, latency: float, traffic: float, distance: float) -> None:
        self.latency_second_link_list.append(latency)
        traffic_per_distance = (traffic * distance)
        self.traffic_per_distance_second_link_list.append(traffic_per_distance)
        self.distance_second_link_list.append(distance)

    def report_second_processing_latency(self, latency: float) -> None:
        self.latency_second_processing_list.append(latency)

    def report_total_finished_latency(self, latency: float) -> None:
        self.latency_total_finished_list.append(latency)
        
    def print_result(self, should_total_be_equal_to_sum_of_parts: bool = True) -> None:
        if should_total_be_equal_to_sum_of_parts:
            # Total should be almost equal to sum of parts (note: also if too few simulation-time or data then it may be false).
            total_as_sum = self.get_average_first_link_latency() + self.get_average_first_processing_latency() + self.get_average_second_link_latency() + self.get_average_second_processing_latency()
            assert abs(self.get_average_total_latency() - total_as_sum) < 0.5

        print(
            f"Finished simulation {self.simulation_name}.\n"
            f"Created packages: {self.data_packages_produced}, "
            f"first link packages {len(self.latency_first_link_list)}, "
            f"first processed packages {len(self.latency_first_processing_list)}, "
            f"second link packages {len(self.latency_second_link_list)}, "
            f"second processed packages {len(self.latency_second_processing_list)}, "
            f"total finished packages {len(self.latency_total_finished_list)}\n"
            f"Average total latency: {self.get_average_total_latency()}\n"
            f"Average first link latency: {self.get_average_first_link_latency()}\n"
            f"Average first processing latency: {self.get_average_first_processing_latency()}\n"
            f"Average second link latency: {self.get_average_second_link_latency()}\n"
            f"Average second processing latency: {self.get_average_second_processing_latency()}\n"
            f"\n"
            f"Total first link traffic per distance: {self.get_total_first_link_traffic_per_distance()}\n"
            f"Total second link traffic per distance: {self.get_total_second_link_traffic_per_distance()}\n"
        )

    def get_average_first_link_latency(self) -> float:
        if len(self.latency_first_link_list) == 0:
            return 0.0
        return statistics.mean(self.latency_first_link_list)

    def get_average_first_processing_latency(self) -> float:
        if len(self.latency_first_processing_list) == 0:
            return 0.0
        return statistics.mean(self.latency_first_processing_list)

    def get_average_second_link_latency(self) -> float:
        if len(self.latency_second_link_list) == 0:
            return 0.0
        return statistics.mean(self.latency_second_link_list)

    def get_average_second_processing_latency(self) -> float:
        if len(self.latency_second_processing_list) == 0:
            return 0.0
        return statistics.mean(self.latency_second_processing_list)

    def get_average_total_latency(self) -> float:
        if len(self.latency_total_finished_list) == 0:
            return 0.0
        return statistics.mean(self.latency_total_finished_list)

    def get_average_total_latency_confidence(self) -> float:
        if len(self.latency_total_finished_list) == 0:
            return 0.0
        z_value = 3.291  # Correspond to 99.9% confidence (probability that true mean is inside this interval).
        std = statistics.stdev(self.latency_total_finished_list)
        num_observations = len(self.latency_total_finished_list)
        return z_value * std / math.sqrt(num_observations)

    def get_total_first_link_traffic_per_distance(self) -> float:
        return sum(self.traffic_per_distance_first_link_list)

    def get_total_second_link_traffic_per_distance(self) -> float:
        return sum(self.traffic_per_distance_second_link_list)

    def get_average_first_link_distance(self) -> float:
        if len(self.distance_first_link_list) == 0:
            return 0.0
        return statistics.mean(self.distance_first_link_list)

    def get_average_second_link_distance(self) -> float:
        if len(self.distance_second_link_list) == 0:
            return 0.0
        return statistics.mean(self.distance_second_link_list)
