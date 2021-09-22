import simpy
from simpy.resources.store import StoreGet

from utils import Utils


SPEED_OF_LIGHT_M_PER_S: float = 299792458.0  # In m/s
SPEED_OF_LIGHT_KM_PER_MS: float = (SPEED_OF_LIGHT_M_PER_S / 1000) / 1000  # In kilometers per millisecond
SPEED_OF_SIGNAL_KM_PER_MS: float = 0.67 * SPEED_OF_LIGHT_KM_PER_MS  # Speed of signal in optical fibers is 67% of the speed of light in vacuum. Ref: https://www.commscope.com/globalassets/digizuite/2799-latency-in-optical-fiber-systems-wp-111432-en.pdf?r=1

# The network near the client is not as fast as the backbone network.
# The wireless connections increase the latency, and it's easy to miss a packet.
EXTRA_MEAN_DELAY_FOR_WEAK_NETWORK = 15.0
EXTRA_STD_DELAY_FOR_WEAK_NETWORK = 5.0

EXTRA_MEAN_DELAY_FOR_ROBUST_NETWORK = 5.0
EXTRA_STD_DELAY_FOR_ROBUST_NETWORK = 1.0


class Transmission(object):
    def __init__(self, simpy_env: simpy.Environment, mean_distance_km: float, std_distance_km: float, is_weak_network: bool):
        self.simpy_env = simpy_env
        self.mean_distance_km = mean_distance_km
        self.std_distance_km = std_distance_km
        self.is_weak_network = is_weak_network
        self.store = simpy.Store(simpy_env, capacity=simpy.core.Infinity)

    def put_in_cable(self, megabytes_of_data: float):
        self.simpy_env.process(self.put_with_latency(megabytes_of_data))

    def get_from_cable(self) -> StoreGet:
        return self.store.get()

    def put_with_latency(self, megabytes_of_data: float):
        delay = self.get_random_cable_delay()
        yield self.simpy_env.timeout(delay)
        self.store.put(megabytes_of_data)

    def get_random_cable_delay(self) -> float:
        distance = Utils.get_random_positive_gaussian_value(mean=self.mean_distance_km, std=self.std_distance_km)
        distance_delay = distance / SPEED_OF_SIGNAL_KM_PER_MS  # time = distance / speed

        if self.is_weak_network:
            network_delay = Utils.get_random_positive_gaussian_value(mean=EXTRA_MEAN_DELAY_FOR_WEAK_NETWORK, std=EXTRA_STD_DELAY_FOR_WEAK_NETWORK)
        else:
            network_delay = Utils.get_random_positive_gaussian_value(mean=EXTRA_MEAN_DELAY_FOR_ROBUST_NETWORK, std=EXTRA_STD_DELAY_FOR_ROBUST_NETWORK)

        return distance_delay + network_delay