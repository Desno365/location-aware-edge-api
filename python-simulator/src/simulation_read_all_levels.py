import multiprocessing
import random
from typing import Dict

import simpy
from matplotlib import pyplot as plt

from result_container import ResultContainer
from src.data_reader import DataReader
from src.processing_units.edge_reader import EdgeReader

SIMULATION_DURATION = 2*60*100  # In milliseconds.
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
    # random.seed(RANDOM_SEED)
    env = simpy.Environment()

    edge_locations = []
    for i in range(NUMBER_OF_LOCATIONS):
        edge_aggregator = EdgeReader(
            simpy_env=env,
            result_container=result_container,
            name=f'Location{i}',
            mean_distance_km=MEAN_DISTANCE_READER_LOCATION,
            std_distance_km=STD_DISTANCE_READER_LOCATION,
            overwrite_number_of_cores=2,
        )
        edge_aggregator.start_listening_for_incoming_data()
        edge_locations.append(edge_aggregator)

    edge_cities = []
    for i in range(NUMBER_OF_CITIES):
        edge_aggregator = EdgeReader(
            simpy_env=env,
            result_container=result_container,
            name=f'City{i}',
            mean_distance_km=MEAN_DISTANCE_READER_CITY,
            std_distance_km=STD_DISTANCE_READER_CITY,
        )
        edge_aggregator.start_listening_for_incoming_data()
        edge_cities.append(edge_aggregator)

    edge_territories = []
    for i in range(NUMBER_OF_TERRITORIES):
        edge_aggregator = EdgeReader(
            simpy_env=env,
            result_container=result_container,
            name=f'Territory{i}',
            mean_distance_km=MEAN_DISTANCE_READER_TERRITORY,
            std_distance_km=STD_DISTANCE_READER_TERRITORY,
        )
        edge_aggregator.start_listening_for_incoming_data()
        edge_territories.append(edge_aggregator)

    edge_countries = []
    for i in range(NUMBER_OF_COUNTRIES):
        edge_aggregator = EdgeReader(
            simpy_env=env,
            result_container=result_container,
            name=f'Country{i}',
            mean_distance_km=MEAN_DISTANCE_READER_COUNTRY,
            std_distance_km=STD_DISTANCE_READER_COUNTRY,
        )
        edge_aggregator.start_listening_for_incoming_data()
        edge_countries.append(edge_aggregator)

    edge_continents = []
    for i in range(NUMBER_OF_CONTINENTS):
        edge_aggregator = EdgeReader(
            simpy_env=env,
            result_container=result_container,
            name=f'Continent{i}',
            mean_distance_km=MEAN_DISTANCE_READER_CONTINENT,
            std_distance_km=STD_DISTANCE_READER_CONTINENT,
            overwrite_number_of_cores=1000,
        )
        edge_aggregator.start_listening_for_incoming_data()
        edge_continents.append(edge_aggregator)

    central = EdgeReader(
            simpy_env=env,
            result_container=result_container,
            name=f'Central',
            mean_distance_km=MEAN_DISTANCE_READER_CENTRAL,
            std_distance_km=STD_DISTANCE_READER_CENTRAL,
            overwrite_number_of_cores=1000,
        )
    central.start_listening_for_incoming_data()

    for i in range(TOTAL_NUMBER_OF_READER_CLIENTS):
        data_producer = DataReader(
            simpy_env=env,
            result_container=result_container,
            name=f'DataProducer{i}',
            probabilities=probabilities,
            transmission_to_location=random.choice(edge_locations).get_incoming_transmission(),
            transmission_to_city=random.choice(edge_cities).get_incoming_transmission(),
            transmission_to_territory=random.choice(edge_territories).get_incoming_transmission(),
            transmission_to_country=random.choice(edge_countries).get_incoming_transmission(),
            transmission_to_continent=random.choice(edge_continents).get_incoming_transmission(),
            transmission_to_central=central.get_incoming_transmission(),
        )
        data_producer.start_reading_data()

    # Run simulation.
    env.run(until=SIMULATION_DURATION)

    result_container.print_result()
    return result_container


pool = multiprocessing.Pool()
results = pool.map(run_configuration, CONFIGURATIONS)

# Prepare plot variables
latencies = [result.get_average_total_latency() for result in results]
# distances = [result.total_read_distance / TOTAL_NUMBER_OF_READER_CLIENTS for result in results]
x_positions_true = range(len(results))
x_positions_scaled = [x / (len(results)-1) for x in range(len(results))]


# Plot total latency.
plt.figure(figsize=(8, 6))
plt.title('Read Latencies')
plt.bar(x_positions_true, latencies, color="green")
plt.axes().yaxis.grid()  # horizontal lines
plt.ylabel("Average Read Latency")
plt.show()
'''
# Plot total distance.
plt.figure(figsize=(8, 6))
plt.title('Read Distances')
plt.bar(x_positions_true, distances, color="green")
plt.axes().yaxis.grid()  # horizontal lines
plt.ylabel("Average Read Distance")
plt.show()
'''
# Plot total latency.
plt.figure(figsize=(8, 6))
plt.title('Read Latencies')
plt.fill_between(x_positions_scaled, latencies)
plt.axes().yaxis.grid()  # horizontal lines
plt.ylabel("Average Read Latency")
plt.show()
'''
# Plot total distance.
plt.figure(figsize=(8, 6))
plt.title('Read Distances')
plt.fill_between(x_positions_scaled, distances)
plt.axes().yaxis.grid()  # horizontal lines
plt.ylabel("Average Read Distance")
plt.show()
'''