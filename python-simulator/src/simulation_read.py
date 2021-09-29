import multiprocessing
import random
from typing import Dict

import numpy as np
import simpy
from matplotlib import pyplot as plt

from src.communication.transmission import Transmission
from src.processing_units.cloud_receiver_and_aggregator import CloudReceiverAndAggregator
from data_producer import DataProducer
from src.processing_units.edge_aggregator import EdgeAggregator
from src.processing_units.edge_receiver import EdgeReceiver
from result_container import ResultContainer

SIMULATION_DURATION = 2*60*1000  # In milliseconds.
RANDOM_SEED = 42
TOTAL_NUMBER_OF_READER_CLIENTS = 10000

NUMBER_OF_LOCATIONS = 5000
MEAN_DISTANCE_READER_LOCATION = 20.0
STD_DISTANCE_READER_LOCATION = 8.0

NUMBER_OF_CITIES = 1000
MEAN_DISTANCE_READER_CITY = 60.0
STD_DISTANCE_READER_CITY = 15.0

NUMBER_OF_TERRITORIES = 400
MEAN_DISTANCE_READER_TERRITORY = 300.0
STD_DISTANCE_READER_TERRITORY = 100.0

NUMBER_OF_COUNTRIES = 150
MEAN_DISTANCE_READER_COUNTRY = 700.0
STD_DISTANCE_READER_COUNTRY = 300.0

NUMBER_OF_CONTINENTS = 7
MEAN_DISTANCE_READER_CONTINENT = 1500.0
STD_DISTANCE_READER_CONTINENT = 500.0

MEAN_DISTANCE_READER_CENTRAL = 5000.0
STD_DISTANCE_READER_CENTRAL = 2000.0

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
            mean_distance_km = MEAN_DISTANCE_READER_LOCATION
            std_distance_km = STD_DISTANCE_READER_LOCATION
        elif extraction - (probabilities[0]+probabilities[1]) <= 0.0:
            mean_distance_km = MEAN_DISTANCE_READER_CITY
            std_distance_km = STD_DISTANCE_READER_CITY
        elif extraction - (probabilities[0]+probabilities[1]+probabilities[2]) <= 0.0:
            mean_distance_km = MEAN_DISTANCE_READER_TERRITORY
            std_distance_km = STD_DISTANCE_READER_TERRITORY
        elif extraction - (probabilities[0]+probabilities[1]+probabilities[2]+probabilities[3]) <= 0.0:
            mean_distance_km = MEAN_DISTANCE_READER_COUNTRY
            std_distance_km = STD_DISTANCE_READER_COUNTRY
        elif extraction - (probabilities[0]+probabilities[1]+probabilities[2]+probabilities[3]+probabilities[4]) <= 0.0:
            mean_distance_km = MEAN_DISTANCE_READER_CONTINENT
            std_distance_km = STD_DISTANCE_READER_CONTINENT
        elif extraction - (probabilities[0]+probabilities[1]+probabilities[2]+probabilities[3]+probabilities[4]+probabilities[5]) <= 0.0:
            mean_distance_km = MEAN_DISTANCE_READER_CENTRAL
            std_distance_km = STD_DISTANCE_READER_CENTRAL

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
