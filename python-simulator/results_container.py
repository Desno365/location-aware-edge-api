class ResultsContainer:

    def __init__(self, simulation_name: str):
        self.simulation_name = simulation_name

        self.data_packages_produced = 0
        
        self.data_packages_passing_first_link = 0
        self.total_latency_first_link = 0.0

        self.data_packages_processed = 0
        self.total_latency_processing = 0.0

        self.data_packages_aggregated = 0
        self.total_latency_from_creation_to_aggregation = 0.0
        
    def print_results(self) -> None:
        print(f"Finished simulation {self.simulation_name}.\n"
              f"Created packages: {self.data_packages_produced}, "
              f"first link packages {self.data_packages_passing_first_link}, "
              f"processed packages {self.data_packages_processed}, "
              f"aggregated packages {self.data_packages_aggregated}\n"
              f"Average total latency: {self.total_latency_from_creation_to_aggregation / self.data_packages_aggregated}\n"
              f"Average first link latency: {self.total_latency_first_link / self.data_packages_passing_first_link}\n"
              f"Average processing latency: {self.total_latency_processing / self.data_packages_processed}\n")
