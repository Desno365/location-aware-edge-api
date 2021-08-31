"use strict";

// Dependencies.
const edgeDb = require("./common/edge-db/edge-db");

// Constants.
const crowdStatusDataDomain = { referringAreaType: "city", ttl: 30*60*1000 }; // 30 minutes TTL.

module.exports = async (event, context) => {
  const videoFootageData = event.body.footage_data;
  const cameraId = event.body.camera_id;
  const crowdStatus = await analyzeCrowdStatus(videoFootageData);
  const response = await edgeDb
      .withDataDomain(crowdStatusDataDomain)
      .set("crowd_" + cameraId, crowdStatus);
  return context
      .status(200)
      .succeed(response);
}

async function analyzeCrowdStatus(videoFootageData) {
  // Implement algorithm to analyze crowd.
  // Here as an example we put directly the result in the footage_data parameter.

  if(videoFootageData > 1.0)
    videoFootageData = 1.0;
  else if(videoFootageData < 0.0)
    videoFootageData = 0.0;

  return videoFootageData;
}
