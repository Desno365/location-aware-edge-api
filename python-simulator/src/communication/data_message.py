import simpy


class DataMessage:

    def __init__(self, megabytes_of_data: float, original_data_creation_time: simpy.core.SimTime, data_sent_time: simpy.core.SimTime):
        self.megabytes_of_data = megabytes_of_data
        self.original_data_creation_time = original_data_creation_time
        self.data_sent_time = data_sent_time
        self.distance_traveled = None
        self.latency_acquired = None

    def set_distance_traveled(self, distance_traveled: float) -> None:
        assert distance_traveled >= 0.0
        self.distance_traveled = distance_traveled

    def set_latency_acquired(self, latency_acquired: float) -> None:
        assert latency_acquired >= 0.0
        self.latency_acquired = latency_acquired
