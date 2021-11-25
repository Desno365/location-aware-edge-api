![politecnico-background](./politecnico-background.png)

# Location-Aware and Stateful Serverless Computing on the Edge

Master of Science Thesis in Computer Science and Engineering at Politecnico di Milano. Academic Year 2020-2021.

## Abstract

The popularity and proliferation of smart devices (e.g., smartphones, wearable devices, Internet-of-Things sensors) is resulting in an unprecedented growth in the amount of collected data. The current most popular approaches to manage this huge amount of data typically rely on cloud platforms located at the core of the infrastructure.

As the number of devices and the amount of data they generate increases, such core-centric approaches are becoming increasingly inefficient as they need to transfer data back and forth between the core and the devices. Furthermore, the latencies associated with such data transfer are affected by the huge travel-distance needed to make the device communicate to the central cloud platform.

To deal with the aforementioned situation new approaches have been introduced in both academia and industry, exploiting the power of the edge of the network to perform the computation closer to the data source. We noticed a discrepancy between the approaches proposed in research and in industry: research frequently assumes the possibility of running virtual machines or long-running containers on the edge. However, most real-world web infrastructure companies do not comply with this assumption due to the limited resource available in the edge.

In this thesis we study the state of the art for stateful computations and data processing on the edge and after carefully analyzing the issues and the needs of the scenario we show the use cases predominantly affected by bandwidth and latency constraints. We then show the current frameworks available in the industry and notice how these solutions do not cover the use cases found. So we then propose a serverless approach effectively applicable by web infrastructure companies, that takes into consideration the problem of the scarcity of the resources, while still allowing quite powerful stateful computations on the edge. We also show how we implemented this new approach through a working prototype, and finally we investigate the gains developers may obtain by using our approach. We demonstrate how several use cases can benefit from this new system through discrete-event simulation, since running our prototype on an emulation of a global edge network was infeasible due to the sheer amount of resources needed to emulate even a small edge network.


## Files

* [Executive Summary](https://github.com/Desno365/location-aware-edge-api/releases/download/thesis-v1.0/Executive_Summary.pdf): a six pages summary of the Thesis.

* [Thesis](https://github.com/Desno365/location-aware-edge-api/releases/download/thesis-v1.0/Thesis.pdf): the main document containing the findings of our work.


## Acknowledgements

Author: [Dennis Motta](https://github.com/Desno365)

Advisor: [Alessandro Margara](https://margara.faculty.polimi.it/)

Co-Advisor: [Gianpaolo Cugola](https://cugola.faculty.polimi.it/)
