"use strict";

// Dependencies.
const edgeDb = require("./common/edge-db/edge-db");

module.exports = async (event, context) => {
  const command = event.body.command;
  const args = event.body.args;
  const reply = await edgeDb.performActionLocally(command, args);
  return context
      .status(200)
      .succeed(reply);
}
