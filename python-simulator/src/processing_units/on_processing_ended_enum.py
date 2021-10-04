from enum import Enum


class OnProcessingEndedEnum(Enum):
    SEND_TO_AGGREGATOR = 1
    SAVE_TOTAL_LATENCY = 2
    DO_NOTHING = 3
