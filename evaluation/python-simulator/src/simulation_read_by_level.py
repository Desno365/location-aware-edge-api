import multiprocessing
import random
from typing import Dict

import simpy
from matplotlib import pyplot as plt

from result_container import ResultContainer
from src import default_architecture_parameters
from src.clients.data_reader_client import DataReaderClient
from src.processing_units.processing_location_central import ProcessingLocationCentral
from src.processing_units.processing_location_city import ProcessingLocationCity
from src.processing_units.processing_location_continent import ProcessingLocationContinent
from src.processing_units.processing_location_country import ProcessingLocationCountry
from src.processing_units.processing_location_district import ProcessingLocationDistrict
from src.processing_units.processing_location_territory import ProcessingLocationTerritory
from src.processing_units.on_processing_ended_enum import OnProcessingEndedEnum

SIMULATION_DURATION = 2*60*1000  # In milliseconds.
TOTAL_NUMBER_OF_READER_CLIENTS = 2000

COMPARED_CONFIGURATION = {
    "aggregation_level": "central",
    "name": "Cloud Aggregation",
}

CONFIGURATIONS = [
    {
        "aggregation_level": "district",
        "name": "District Aggregation",
    },
    {
        "aggregation_level": "city",
        "name": "City Aggregation",
    },
    {
        "aggregation_level": "territory",
        "name": "Territory Aggregation",
    },
    {
        "aggregation_level": "country",
        "name": "Country Aggregation",
    },
    {
        "aggregation_level": "continent",
        "name": "Continent Aggregation",
    },
]


def run_configuration(config: Dict) -> ResultContainer:
    aggregation_level = config['aggregation_level']
    print(f"################## Running configuration: {aggregation_level}")

    # Setup the simulation.
    result_container = ResultContainer(simulation_name=config['name'], simulation_type=aggregation_level)
    env = simpy.Environment()

    edge_locations = []
    if aggregation_level == "district":
        for i in range(default_architecture_parameters.NUMBER_OF_DISTRICTS):
            edge_district = ProcessingLocationDistrict(
                simpy_env=env,
                result_container=result_container,
                name=f'Location{i}',
                mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_CLIENT_DISTRICT,
                std_distance_km=default_architecture_parameters.STD_DISTANCE_CLIENT_DISTRICT,
                on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
            )
            edge_district.start_listening_for_incoming_data()
            edge_locations.append(edge_district)
    elif aggregation_level == "city":
        for i in range(default_architecture_parameters.NUMBER_OF_CITIES):
            edge_city = ProcessingLocationCity(
                simpy_env=env,
                result_container=result_container,
                name=f'City{i}',
                is_data_coming_from_first_link=True,
                mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_CLIENT_CITY,
                std_distance_km=default_architecture_parameters.STD_DISTANCE_CLIENT_CITY,
                on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
            )
            edge_city.start_listening_for_incoming_data()
            edge_locations.append(edge_city)
    elif aggregation_level == "territory":
        for i in range(default_architecture_parameters.NUMBER_OF_TERRITORIES):
            edge_territory = ProcessingLocationTerritory(
                simpy_env=env,
                result_container=result_container,
                name=f'Territory{i}',
                is_data_coming_from_first_link=True,
                mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_CLIENT_TERRITORY,
                std_distance_km=default_architecture_parameters.STD_DISTANCE_CLIENT_TERRITORY,
                on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
            )
            edge_territory.start_listening_for_incoming_data()
            edge_locations.append(edge_territory)
    elif aggregation_level == "country":
        for i in range(default_architecture_parameters.NUMBER_OF_COUNTRIES):
            edge_country = ProcessingLocationCountry(
                simpy_env=env,
                result_container=result_container,
                name=f'Country{i}',
                is_data_coming_from_first_link=True,
                mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_CLIENT_COUNTRY,
                std_distance_km=default_architecture_parameters.STD_DISTANCE_CLIENT_COUNTRY,
                on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
            )
            edge_country.start_listening_for_incoming_data()
            edge_locations.append(edge_country)
    elif aggregation_level == "continent":
        for i in range(default_architecture_parameters.NUMBER_OF_CONTINENTS):
            edge_continent = ProcessingLocationContinent(
                simpy_env=env,
                result_container=result_container,
                name=f'Continent{i}',
                is_data_coming_from_first_link=True,
                mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_CLIENT_CONTINENT,
                std_distance_km=default_architecture_parameters.STD_DISTANCE_CLIENT_CONTINENT,
                on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
            )
            edge_continent.start_listening_for_incoming_data()
            edge_locations.append(edge_continent)
    elif aggregation_level == "central":
        central = ProcessingLocationCentral(
            simpy_env=env,
            result_container=result_container,
            name=f'Central',
            is_data_coming_from_first_link=True,
            mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_CLIENT_CENTRAL,
            std_distance_km=default_architecture_parameters.STD_DISTANCE_CLIENT_CENTRAL,
            on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
        )
        central.start_listening_for_incoming_data()
        edge_locations.append(central)
    else:
        raise Exception("Aggregation not recognized.")

    for i in range(TOTAL_NUMBER_OF_READER_CLIENTS):
        data_producer = DataReaderClient(
            simpy_env=env,
            result_container=result_container,
            name=f'DataProducerClient{i}',
            use_single_transmission=True,
            transmission=random.choice(edge_locations).get_incoming_transmission(),
        )
        data_producer.start_reading_data()

    # Run simulation.
    env.run(until=SIMULATION_DURATION)

    result_container.print_result()
    return result_container


result_central = run_configuration(COMPARED_CONFIGURATION)

pool = multiprocessing.Pool()
results = pool.map(run_configuration, CONFIGURATIONS)

for result in results:
    # Prepare plot variables
    total_latencies = [result.get_average_total_latency(), result_central.get_average_total_latency()]
    names = [result.simulation_name, result_central.simulation_name]
    colors = ["green", "red"]
    x_positions = (range(len(total_latencies)))

    # Plot total latency.
    plt.figure(figsize=(5, 4))
    plt.title(f'Read Latencies for {result.simulation_name}')
    plt.bar(x_positions, total_latencies, width=0.666, color=colors)
    plt.axes().yaxis.grid()  # horizontal lines
    plt.xticks(x_positions, names)
    plt.ylabel("Average Read Latency")
    plt.tight_layout()
    plt.savefig(f'read-by-latency-{result.simulation_name.replace(" ", "-")}.png')
    #plt.show()

for result in results:
    # Prepare plot variables
    total_distances = [result.get_average_first_link_distance() + result.get_average_second_link_distance(), result_central.get_average_first_link_distance() + result_central.get_average_second_link_distance()]
    names = [result.simulation_name, result_central.simulation_name]
    colors = ["green", "red"]
    x_positions = (range(len(total_distances)))

    # Plot total distance.
    plt.figure(figsize=(5, 4))
    plt.title(f'Read Distances for {result.simulation_name}')
    plt.bar(x_positions, total_distances, width=0.666, color=colors)
    plt.axes().yaxis.grid()  # horizontal lines
    plt.xticks(x_positions, names)
    plt.ylabel("Average Read Distance")
    plt.tight_layout()
    plt.savefig(f'read-by-distance-{result.simulation_name.replace(" ", "-")}.png')
    #plt.show()
