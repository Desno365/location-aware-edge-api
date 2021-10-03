import multiprocessing
import random
from typing import Dict

import simpy
from matplotlib import pyplot as plt

from result_container import ResultContainer
from src import architecture_parameters
from src.data_reader import DataReader
from src.processing_units.edge_location_central import EdgeLocationCentral
from src.processing_units.edge_location_city import EdgeLocationCity
from src.processing_units.edge_location_continent import EdgeLocationContinent
from src.processing_units.edge_location_country import EdgeLocationCountry
from src.processing_units.edge_location_district import EdgeLocationDistrict
from src.processing_units.edge_location_territory import EdgeLocationTerritory

SIMULATION_DURATION = 2*60*100  # In milliseconds.
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
    # random.seed(RANDOM_SEED)
    env = simpy.Environment()

    edge_districts = []
    for i in range(architecture_parameters.NUMBER_OF_DISTRICTS):
        edge_district = EdgeLocationDistrict(
            simpy_env=env,
            result_container=result_container,
            name=f'Location{i}',
            mean_distance_km=architecture_parameters.MEAN_DISTANCE_CLIENT_DISTRICT,
            std_distance_km=architecture_parameters.STD_DISTANCE_CLIENT_DISTRICT,
            should_send_processed_data_to_aggregator=False,
        )
        edge_district.start_listening_for_incoming_data()
        edge_districts.append(edge_district)

    edge_cities = []
    for i in range(architecture_parameters.NUMBER_OF_CITIES):
        edge_city = EdgeLocationCity(
            simpy_env=env,
            result_container=result_container,
            name=f'City{i}',
            is_data_coming_from_first_link=True,
            mean_distance_km=architecture_parameters.MEAN_DISTANCE_CLIENT_CITY,
            std_distance_km=architecture_parameters.STD_DISTANCE_CLIENT_CITY,
            should_send_processed_data_to_aggregator=False,
        )
        edge_city.start_listening_for_incoming_data()
        edge_cities.append(edge_city)

    edge_territories = []
    for i in range(architecture_parameters.NUMBER_OF_TERRITORIES):
        edge_territory = EdgeLocationTerritory(
            simpy_env=env,
            result_container=result_container,
            name=f'Territory{i}',
            is_data_coming_from_first_link=True,
            mean_distance_km=architecture_parameters.MEAN_DISTANCE_CLIENT_TERRITORY,
            std_distance_km=architecture_parameters.STD_DISTANCE_CLIENT_TERRITORY,
            should_send_processed_data_to_aggregator=False,
        )
        edge_territory.start_listening_for_incoming_data()
        edge_territories.append(edge_territory)

    edge_countries = []
    for i in range(architecture_parameters.NUMBER_OF_COUNTRIES):
        edge_country = EdgeLocationCountry(
            simpy_env=env,
            result_container=result_container,
            name=f'Country{i}',
            is_data_coming_from_first_link=True,
            mean_distance_km=architecture_parameters.MEAN_DISTANCE_CLIENT_COUNTRY,
            std_distance_km=architecture_parameters.STD_DISTANCE_CLIENT_COUNTRY,
            should_send_processed_data_to_aggregator=False,
        )
        edge_country.start_listening_for_incoming_data()
        edge_countries.append(edge_country)

    edge_continents = []
    for i in range(architecture_parameters.NUMBER_OF_CONTINENTS):
        edge_continent = EdgeLocationContinent(
            simpy_env=env,
            result_container=result_container,
            name=f'Continent{i}',
            is_data_coming_from_first_link=True,
            mean_distance_km=architecture_parameters.MEAN_DISTANCE_CLIENT_CONTINENT,
            std_distance_km=architecture_parameters.STD_DISTANCE_CLIENT_CONTINENT,
            should_send_processed_data_to_aggregator=False,
        )
        edge_continent.start_listening_for_incoming_data()
        edge_continents.append(edge_continent)

    central = EdgeLocationCentral(
        simpy_env=env,
        result_container=result_container,
        name=f'Central',
        is_data_coming_from_first_link=True,
        mean_distance_km=architecture_parameters.MEAN_DISTANCE_CLIENT_CENTRAL,
        std_distance_km=architecture_parameters.STD_DISTANCE_CLIENT_CENTRAL,
        should_send_processed_data_to_aggregator=False,
    )
    central.start_listening_for_incoming_data()

    for i in range(TOTAL_NUMBER_OF_READER_CLIENTS):
        data_producer = DataReader(
            simpy_env=env,
            result_container=result_container,
            name=f'DataProducer{i}',
            probabilities=probabilities,
            transmission_to_district=random.choice(edge_districts).get_incoming_transmission(),
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