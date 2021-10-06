"use strict";

// Dependencies.
const edgeDb = require("./common/edge-db/edgeDb");

// Constants.
const ioTDataDomain = { referringAreaType: "location", ttl: 2*24*60*60*1000 }; // 2 days TTL.

module.exports = async (event, context) => {
  const iotData = event.body.iot_data;
  const previousIotData = await edgeDb.get("latest_iot_data");

  if(iotData !== previousIotData) {
    const reply = await edgeDb
        .withDataDomain(ioTDataDomain)
        .set("latest_iot_data", iotData);
    // Send value to the cloud.

    return context
        .status(200)
        .succeed('Value updated.');
  } else {
    return context
        .status(200)
        .succeed('Value not changed.');
  }
}
