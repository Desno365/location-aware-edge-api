import multiprocessing
import random
from typing import Dict

from matplotlib import pyplot as plt

from result_container import ResultContainer
from src import architecture_parameters
from src.communication.transmission import Transmission

RANDOM_SEED = 42
TOTAL_NUMBER_OF_READER_CLIENTS = 10000

CONFIGURATIONS = [
    {"probabilities": [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]},
    {"probabilities": [0.8, 0.2, 0.0, 0.0, 0.0, 0.0]},
    {"probabilities": [0.8, 0.0, 0.2, 0.0, 0.0, 0.0]},
    {"probabilities": [0.8, 0.0, 0.0, 0.2, 0.0, 0.0]},
    {"probabilities": [0.8, 0.0, 0.0, 0.0, 0.2, 0.0]},
    {"probabilities": [0.8, 0.0, 0.0, 0.0, 0.0, 0.2]},
    {"probabilities": [0.6, 0.2, 0.0, 0.0, 0.0, 0.2]},
    {"probabilities": [0.6, 0.0, 0.2, 0.0, 0.0, 0.2]},
    {"probabilities": [0.6, 0.0, 0.0, 0.2, 0.0, 0.2]},
    {"probabilities": [0.6, 0.0, 0.0, 0.0, 0.2, 0.2]},
    {"probabilities": [0.4, 0.2, 0.0, 0.0, 0.2, 0.2]},
    {"probabilities": [0.4, 0.0, 0.2, 0.0, 0.2, 0.2]},
    {"probabilities": [0.4, 0.0, 0.0, 0.2, 0.2, 0.2]},
    {"probabilities": [0.2, 0.2, 0.0, 0.2, 0.2, 0.2]},
    {"probabilities": [0.2, 0.0, 0.2, 0.2, 0.2, 0.2]},
    {"probabilities": [0.0, 0.2, 0.2, 0.2, 0.2, 0.2]},
    {"probabilities": [0.0, 0.0, 0.4, 0.2, 0.2, 0.2]},
    {"probabilities": [0.0, 0.0, 0.2, 0.4, 0.2, 0.2]},
    {"probabilities": [0.0, 0.0, 0.2, 0.2, 0.4, 0.2]},
    {"probabilities": [0.0, 0.0, 0.2, 0.2, 0.2, 0.4]},
    {"probabilities": [0.0, 0.0, 0.0, 0.4, 0.2, 0.4]},
    {"probabilities": [0.0, 0.0, 0.0, 0.2, 0.4, 0.4]},
    {"probabilities": [0.0, 0.0, 0.0, 0.0, 0.6, 0.4]},
    {"probabilities": [0.0, 0.0, 0.0, 0.0, 0.4, 0.6]},
    {"probabilities": [0.0, 0.0, 0.0, 0.0, 0.2, 0.8]},
    {"probabilities": [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]},
]


def run_configuration(config: Dict) -> ResultContainer:
    probabilities = config['probabilities']
    print(f"################## Running configuration: {probabilities}")

    # Setup the simulation.
    result_container = ResultContainer(simulation_name=config['probabilities'], simulation_type="read")
    random.seed(RANDOM_SEED)

    # Run simulation.
    for _ in range(TOTAL_NUMBER_OF_READER_CLIENTS):
        mean_distance_km = None
        std_distance_km = None
        extraction = random.uniform(0.0, 1.0)
        if extraction - (probabilities[0]) <= 0.0:
            mean_distance_km = architecture_parameters.MEAN_DISTANCE_CLIENT_DISTRICT
            std_distance_km = architecture_parameters.STD_DISTANCE_CLIENT_DISTRICT
        elif extraction - (probabilities[0]+probabilities[1]) <= 0.0:
            mean_distance_km = architecture_parameters.MEAN_DISTANCE_CLIENT_CITY
            std_distance_km = architecture_parameters.STD_DISTANCE_CLIENT_CITY
        elif extraction - (probabilities[0]+probabilities[1]+probabilities[2]) <= 0.0:
            mean_distance_km = architecture_parameters.MEAN_DISTANCE_CLIENT_TERRITORY
            std_distance_km = architecture_parameters.STD_DISTANCE_CLIENT_TERRITORY
        elif extraction - (probabilities[0]+probabilities[1]+probabilities[2]+probabilities[3]) <= 0.0:
            mean_distance_km = architecture_parameters.MEAN_DISTANCE_CLIENT_COUNTRY
            std_distance_km = architecture_parameters.STD_DISTANCE_CLIENT_COUNTRY
        elif extraction - (probabilities[0]+probabilities[1]+probabilities[2]+probabilities[3]+probabilities[4]) <= 0.0:
            mean_distance_km = architecture_parameters.MEAN_DISTANCE_CLIENT_CONTINENT
            std_distance_km = architecture_parameters.STD_DISTANCE_CLIENT_CONTINENT
        elif extraction - (probabilities[0]+probabilities[1]+probabilities[2]+probabilities[3]+probabilities[4]+probabilities[5]) <= 0.0:
            mean_distance_km = architecture_parameters.MEAN_DISTANCE_CLIENT_CENTRAL
            std_distance_km = architecture_parameters.STD_DISTANCE_CLIENT_CENTRAL

        distance, delay = Transmission.get_cable_distance_and_delay(mean_distance_km=mean_distance_km, std_distance_km=std_distance_km, is_weak_network=True)
        result_container.total_read_distance += distance
        result_container.total_read_latency += delay
    return result_container


pool = multiprocessing.Pool()
results = pool.map(run_configuration, CONFIGURATIONS)

# Prepare plot variables
latencies = [result.total_read_latency / TOTAL_NUMBER_OF_READER_CLIENTS for result in results]
distances = [result.total_read_distance / TOTAL_NUMBER_OF_READER_CLIENTS for result in results]
x_positions_true = range(len(results))
x_positions_scaled = [x / (len(results)-1) for x in range(len(results))]


# Plot total latency.
plt.figure(figsize=(8, 6))
plt.title('Read Latencies')
plt.bar(x_positions_true, latencies, color="green")
plt.axes().yaxis.grid()  # horizontal lines
plt.ylabel("Average Read Latency")
plt.show()

# Plot total distance.
plt.figure(figsize=(8, 6))
plt.title('Read Distances')
plt.bar(x_positions_true, distances, color="green")
plt.axes().yaxis.grid()  # horizontal lines
plt.ylabel("Average Read Distance")
plt.show()

# Plot total latency.
plt.figure(figsize=(8, 6))
plt.title('Read Latencies')
plt.fill_between(x_positions_scaled, latencies)
plt.axes().yaxis.grid()  # horizontal lines
plt.ylabel("Average Read Latency")
plt.show()

# Plot total distance.
plt.figure(figsize=(8, 6))
plt.title('Read Distances')
plt.fill_between(x_positions_scaled, distances)
plt.axes().yaxis.grid()  # horizontal lines
plt.ylabel("Average Read Distance")
plt.show()
