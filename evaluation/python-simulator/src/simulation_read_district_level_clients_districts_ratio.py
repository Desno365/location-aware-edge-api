import multiprocessing
import random
from typing import Dict

import simpy
from matplotlib import pyplot as plt

from result_container import ResultContainer
from src import default_architecture_parameters
from src.clients.data_reader_client import DataReaderClient
from src.processing_units.processing_location_central import ProcessingLocationCentral
from src.processing_units.processing_location_district import ProcessingLocationDistrict
from src.processing_units.on_processing_ended_enum import OnProcessingEndedEnum

#default_architecture_parameters.NUMBER_OF_DISTRICTS = 200  # Overwrite number of districts (with 1000 goes out of RAM :( ).
TOTAL_PACKAGES_READ_BY_EACH_CLIENT = 1  # Note: each client has a waiting time before reading a new data.
CLIENTS_DISTRICTS_RATIO_RANGE = range(2, 4000, 501)  # start, end, step
print(list(CLIENTS_DISTRICTS_RATIO_RANGE))

CONFIGURATIONS_EDGE = [{"ratio": i, "type": "edge"} for i in CLIENTS_DISTRICTS_RATIO_RANGE]
CONFIGURATIONS_CLOUD = [{"ratio": i, "type": "cloud"} for i in CLIENTS_DISTRICTS_RATIO_RANGE]


def run_configuration(config: Dict) -> ResultContainer:
    ratio = config['ratio']
    number_of_clients = default_architecture_parameters.NUMBER_OF_DISTRICTS * ratio
    print(f"################## Running configuration: {ratio}")

    # Setup the simulation.
    result_container = ResultContainer(simulation_name=str(ratio), simulation_type=config['type'])
    env = simpy.Environment()

    edge_locations = []
    if config["type"] == "edge":
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
    elif config["type"] == "cloud":  # If cloud, setup the cloud and data_producers
        cloud = ProcessingLocationCentral(
            simpy_env=env,
            result_container=result_container,
            name="Cloud",
            is_data_coming_from_first_link=True,
            mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_CLIENT_CENTRAL,
            std_distance_km=default_architecture_parameters.STD_DISTANCE_CLIENT_CENTRAL,
            on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
        )
        cloud.start_listening_for_incoming_data()
        edge_locations.append(cloud)
    else:
        raise Exception('Type not recognized')

    for i in range(number_of_clients):
        data_reader = DataReaderClient(
            simpy_env=env,
            result_container=result_container,
            name=f'DataProducerClient{i}',
            use_single_transmission=True,
            transmission=random.choice(edge_locations).get_incoming_transmission(),
            number_of_packages_to_read=TOTAL_PACKAGES_READ_BY_EACH_CLIENT,
        )
        data_reader.start_reading_data()

    # Run simulation.
    env.run()

    result_container.print_result()
    return result_container


pool = multiprocessing.Pool()
results_edge = pool.map(run_configuration, CONFIGURATIONS_EDGE)

pool = multiprocessing.Pool()
results_cloud = pool.map(run_configuration, CONFIGURATIONS_CLOUD)

# Prepare plot variables
total_latencies_edge = [result.get_average_total_latency() for result in results_edge]
total_latencies_cloud = [result.get_average_total_latency() for result in results_cloud]
total_distance_edge = [result.get_average_first_link_distance() + result.get_average_second_link_distance() for result in results_edge]
total_distance_cloud = [result.get_average_first_link_distance() + result.get_average_second_link_distance() for result in results_cloud]
x_positions = [default_architecture_parameters.NUMBER_OF_DISTRICTS * i for i in CLIENTS_DISTRICTS_RATIO_RANGE]

# Plot total latency.
plt.figure(figsize=(8, 6))
plt.title('Read Latencies')
plt.plot(x_positions, total_latencies_edge, color="green")
plt.plot(x_positions, total_latencies_cloud, color="red")
plt.axes().yaxis.grid()  # horizontal lines
plt.axes().set_xlim([0, None])
plt.axes().set_ylim([0, None])
plt.xlabel("Number of clients")
plt.ylabel("Average Read Latency")
plt.legend(["Edge solution", "Cloud solution"])
plt.tight_layout()
plt.show()

# Plot sum of traffic uncut.
plt.figure(figsize=(8, 6))
plt.title('Read Distances')
plt.plot(x_positions, total_distance_edge, color="green")
plt.plot(x_positions, total_distance_cloud, color="red")
plt.axes().yaxis.grid()  # horizontal lines
plt.axes().set_xlim([0, None])
plt.axes().set_ylim([0, None])
plt.xlabel("Number of clients")
plt.ylabel("Average Read Distance")
plt.legend(["Edge solution", "Cloud solution"])
plt.tight_layout()
plt.show()
