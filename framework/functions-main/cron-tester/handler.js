"use strict";

// Dependencies.
const edgeDb = require("./common/edge-db/edgeDb");

module.exports = async (event, context) => {
  const latestData = await edgeDb.get("latest_iot_data");
  console.log("Latest data: " + latestData);

  return context
      .status(200)
      .succeed('Executed.');
}
