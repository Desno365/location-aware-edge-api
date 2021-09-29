class ResultContainer:

    def __init__(self, simulation_name: str, simulation_type: str):
        self.simulation_name = simulation_name
        self.simulation_type = simulation_type

        self.data_packages_produced = 0

        # Latencies variables.
        
        self.data_packages_passing_first_link = 0
        self.total_latency_first_link = 0.0

        self.data_packages_passing_first_processing = 0
        self.total_latency_first_processing = 0.0

        self.data_packages_passing_second_link = 0
        self.total_latency_second_link = 0.0

        self.data_packages_passing_second_processing = 0
        self.total_latency_second_processing = 0.0

        self.data_packages_aggregated = 0
        self.total_latency_from_creation_to_aggregation = 0.0

        # Traffic variables.
        self.traffic_per_distance_first_link = 0.0
        self.traffic_per_distance_second_link = 0.0
        
    def print_result(self) -> None:
        total_as_sum = self.get_average_first_link_latency() + self.get_average_first_processing_latency() + self.get_average_second_link_latency() + self.get_average_second_processing_latency()
        assert abs(self.get_average_total_latency() - total_as_sum) < 0.5  # Total should be almost equal to sum of parts (note: if too few time or data then it may be false).

        print(f"Finished simulation {self.simulation_name}.\n"
              f"Created packages: {self.data_packages_produced}, "
              f"first link packages {self.data_packages_passing_first_link}, "
              f"first processed packages {self.data_packages_passing_first_processing}, "
              f"second link packages {self.data_packages_passing_second_link}, "
              f"second processed packages {self.data_packages_passing_second_processing}, "
              f"aggregated packages {self.data_packages_aggregated}\n"
              f"Average total latency: {self.get_average_total_latency()}\n"
              f"Average first link latency: {self.get_average_first_link_latency()}\n"
              f"Average first processing latency: {self.get_average_first_processing_latency()}\n"
              f"Average second link latency: {self.get_average_second_link_latency()}\n"
              f"Average second processing latency: {self.get_average_second_processing_latency()}\n"
              f"\n"
              f"Average first link traffic per distance: {self.get_average_first_link_traffic_per_distance()}\n"
              f"Average second link traffic per distance: {self.get_average_second_link_traffic_per_distance()}\n"
        )


    def get_average_total_latency(self) -> float:
        return self.total_latency_from_creation_to_aggregation / self.data_packages_aggregated

    def get_average_first_link_latency(self) -> float:
        return self.total_latency_first_link / self.data_packages_passing_first_link

    def get_average_first_processing_latency(self) -> float:
        return self.total_latency_first_processing / self.data_packages_passing_first_processing

    def get_average_second_link_latency(self) -> float:
        if self.data_packages_passing_second_link <= 0:
            return 0.0
        else:
            return self.total_latency_second_link / self.data_packages_passing_second_link

    def get_average_second_processing_latency(self) -> float:
        if self.data_packages_passing_second_processing <= 0:
            return 0.0
        else:
            return self.total_latency_second_processing / self.data_packages_passing_second_processing


    def get_average_first_link_traffic_per_distance(self) -> float:
        return self.traffic_per_distance_first_link / self.data_packages_passing_first_link

    def get_average_second_link_traffic_per_distance(self) -> float:
        if self.data_packages_passing_second_link <= 0:
            return 0.0
        else:
            return self.traffic_per_distance_second_link / self.data_packages_passing_second_link
