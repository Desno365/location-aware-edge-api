import random


class Utils:
    PRINT_TIME_MESSAGES = False

    @staticmethod
    def get_random_positive_gaussian_value(mean: float, std: float) -> float:
        value = None
        while value is None or value < 0.0:
            value = random.gauss(mean, std)
        return value
