import random


class Utils:
    PRINT_TIME_MESSAGES = False

    total_number_of_data_packages_produced = 0
    total_number_of_data_packages_processed = 0

    @staticmethod
    def get_random_positive_gaussian_value(mean: float, std: float) -> float:
        value = None
        while value is None or value < 0.0:
            value = random.gauss(mean, std)
        return value
