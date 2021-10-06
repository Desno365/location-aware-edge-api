"use strict";

// Dependencies.
const edgeDb = require("./common/edge-db/edgeDb");

module.exports = async (event, context) => {
  const startingPoint = event.body.starting_point;
  const destinationPoint = event.body.destination_point;

  const cameraIds = await getCameraIdsForPossiblePaths(startingPoint, destinationPoint);
  const crowdStatuses = [];
  for(const cameraId of cameraIds) {
    const crowdStatus = await edgeDb.get("crowd_" + cameraId);
    if(crowdStatus === null || crowdStatus === undefined)
      crowdStatuses.push(1.0);
    else
      crowdStatuses.push(crowdStatus);
  }

  const bestPath = await computeBestPath(cameraIds, crowdStatuses);

  return context
      .status(200)
      .succeed(bestPath);
}

async function getCameraIdsForPossiblePaths(startingPoint, destinationPoint) {
  // Implement algorithm to get the list of the possible cameras to be analyzed for possible paths.
  return ["camera1", "camera2", "camera3"];
}

async function computeBestPath(cameraIds, crowdStatuses) {
  // Find first.
  let indexOfFirstLessCrowded;
  let firstLessCrowdedStatus = 1.001;
  for (let i = 0; i < crowdStatuses.length ; i++) {
    const crowdStatus = crowdStatuses[i];
    if(crowdStatus < firstLessCrowdedStatus) {
      firstLessCrowdedStatus = crowdStatus;
      indexOfFirstLessCrowded = i;
    }
  }

  // Find second.
  let indexOfSecondLessCrowded;
  let secondLessCrowdedStatus = 1.001;
  for (let i = 0; i < crowdStatuses.length ; i++) {
    const crowdStatus = crowdStatuses[i];
    if(crowdStatus < secondLessCrowdedStatus && i !== indexOfFirstLessCrowded) {
      secondLessCrowdedStatus = crowdStatus;
      indexOfSecondLessCrowded = i;
    }
  }

  return [cameraIds[indexOfFirstLessCrowded], cameraIds[indexOfSecondLessCrowded]];
}
