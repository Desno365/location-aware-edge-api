import math
from typing import Tuple

import simpy
from simpy.resources.store import StoreGet

from src.communication.data_message import DataMessage
from src.utils import Utils

SPEED_OF_LIGHT_M_PER_S: float = 299792458.0  # In m/s
SPEED_OF_LIGHT_KM_PER_MS: float = (SPEED_OF_LIGHT_M_PER_S / 1000) / 1000  # In kilometers per millisecond
OPTICAL_FIBER_OFFSET = 0.67  # Speed of signal in optical fibers is 67% of the speed of light in vacuum. Ref: https://www.commscope.com/globalassets/digizuite/2799-latency-in-optical-fiber-systems-wp-111432-en.pdf?r=1
ROUND_TRIP_OFFSET = 0.50  # Round trip makes the signal go back and forth.
NO_LINE_OF_SIGHT_OFFSET = 1 / math.sqrt(2)  # ≈0.707  # The cables cannot make a direct path.
SPEED_OF_SIGNAL_KM_PER_MS: float = SPEED_OF_LIGHT_KM_PER_MS * NO_LINE_OF_SIGHT_OFFSET * ROUND_TRIP_OFFSET * OPTICAL_FIBER_OFFSET

# The network near the client is not as fast as the backbone network.
# The wireless connections increase the latency, and it's easy to miss a packet.
EXTRA_MEAN_DELAY_FOR_WEAK_NETWORK = 12.0
EXTRA_STD_DELAY_FOR_WEAK_NETWORK = 8.0

EXTRA_MEAN_DELAY_FOR_ROBUST_NETWORK = 3.0
EXTRA_STD_DELAY_FOR_ROBUST_NETWORK = 1.0


class Transmission(object):
    def __init__(self, simpy_env: simpy.Environment, mean_distance_km: float, std_distance_km: float, has_weak_network_initial_delay: bool):
        assert simpy_env is not None
        assert mean_distance_km > 0.0
        assert std_distance_km > 0.0
        assert has_weak_network_initial_delay is True or has_weak_network_initial_delay is False

        self.simpy_env = simpy_env
        self.mean_distance_km = mean_distance_km
        self.std_distance_km = std_distance_km
        self.is_weak_network = has_weak_network_initial_delay
        self.store = simpy.Store(simpy_env, capacity=simpy.core.Infinity)

    def put_in_cable(self, message: DataMessage):
        self.simpy_env.process(self.put_with_latency(message))

    def get_from_cable(self) -> StoreGet:
        return self.store.get()

    def put_with_latency(self, message: DataMessage):
        distance, delay = Transmission.get_cable_distance_and_delay(mean_distance_km=self.mean_distance_km, std_distance_km=self.std_distance_km, is_weak_network=self.is_weak_network)
        message.set_distance_traveled(distance)
        message.set_latency_acquired(delay)
        yield self.simpy_env.timeout(delay)
        self.store.put(message)

    @staticmethod
    def get_cable_distance_and_delay(mean_distance_km: float, std_distance_km: float, is_weak_network: bool) -> Tuple[float, float]:
        if is_weak_network:
            network_delay = Utils.get_random_positive_gaussian_value(mean=EXTRA_MEAN_DELAY_FOR_WEAK_NETWORK,
                                                                     std=EXTRA_STD_DELAY_FOR_WEAK_NETWORK)
        else:
            network_delay = Utils.get_random_positive_gaussian_value(mean=EXTRA_MEAN_DELAY_FOR_ROBUST_NETWORK,
                                                                     std=EXTRA_STD_DELAY_FOR_ROBUST_NETWORK)

        distance = Utils.get_random_positive_gaussian_value(mean=mean_distance_km, std=std_distance_km)
        distance_delay = distance / SPEED_OF_SIGNAL_KM_PER_MS  # time = distance / speed

        return distance, (network_delay + distance_delay)
