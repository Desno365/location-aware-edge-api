import multiprocessing
import random
from typing import Dict

import numpy as np
import simpy
from matplotlib import pyplot as plt

from result_container import ResultContainer
from src import default_architecture_parameters
from src.clients.data_reader import DataReader
from src.processing_units.edge_location_central import EdgeLocationCentral
from src.processing_units.edge_location_district import EdgeLocationDistrict
from src.processing_units.on_processing_ended_enum import OnProcessingEndedEnum

TOTAL_NUMBER_OF_READER_CLIENTS = 2000
TOTAL_PACKAGES_READ_BY_EACH_CLIENT = 2  # Note: each client has a waiting time before reading a new data.
BANDWIDTH_RATIO_RANGE = np.linspace(0.01, 1, 64)  # start, end, num_of_points
print(BANDWIDTH_RATIO_RANGE)

CONFIGURATIONS = [{"ratio": i, "type": "edge"} for i in BANDWIDTH_RATIO_RANGE]


def run_configuration(config: Dict) -> ResultContainer:
    ratio = config['ratio']
    print(f"################## Running configuration: {ratio}")

    # Setup the simulation.
    result_container = ResultContainer(simulation_name=str(ratio), simulation_type=config['type'])
    env = simpy.Environment()

    edge_locations = []
    if config["type"] == "edge":
        for i in range(default_architecture_parameters.NUMBER_OF_DISTRICTS):
            edge_district = EdgeLocationDistrict(
                simpy_env=env,
                result_container=result_container,
                name=f'Location{i}',
                mean_distance_km=default_architecture_parameters.MEAN_DISTANCE_CLIENT_DISTRICT,
                std_distance_km=default_architecture_parameters.STD_DISTANCE_CLIENT_DISTRICT,
                on_processing_ended_specification=OnProcessingEndedEnum.SAVE_TOTAL_LATENCY,
                override_bandwidth=ratio * default_architecture_parameters.BANDWIDTH_CAPABILITY_CENTRAL,
            )
            edge_district.start_listening_for_incoming_data()
            edge_locations.append(edge_district)
    elif config["type"] == "cloud":  # If cloud, setup the cloud and data_producers
        cloud = EdgeLocationCentral(
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

    for i in range(TOTAL_NUMBER_OF_READER_CLIENTS):
        data_reader = DataReader(
            simpy_env=env,
            result_container=result_container,
            name=f'DataProducer{i}',
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
results = pool.map(run_configuration, CONFIGURATIONS)

# Prepare plot variables
total_latencies = np.array([result.get_average_total_latency() for result in results])
total_latencies_confidence = np.array([result.get_average_total_latency_confidence() for result in results])
x_positions = [i for i in BANDWIDTH_RATIO_RANGE]

# Plot total latency.
plt.figure(figsize=(8, 6))
plt.title('Read Latencies')
plt.plot(x_positions, total_latencies, color="green")
plt.axes().set_xlim([0, None])
plt.axes().set_ylim([0, None])
plt.ylabel("Average Read Latency")
plt.tight_layout()
plt.show()

#'''
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_title('Read Latencies')
ax.set_ylabel('Average Read Latency')
ax.plot(x_positions, total_latencies, color="green")
ax.fill_between(x_positions, (total_latencies - total_latencies_confidence), (total_latencies + total_latencies_confidence), color="green", alpha=0.1)
ax.set_xlim([0, None])
ax.set_ylim([0, None])
fig.tight_layout()
fig.show()
#'''
