"use strict"

const redis = require("redis");
const { promisify } = require("util");

module.exports = async (event, context) => {
  console.log("Using redis ip " + process.env.REDIS_IP + " and port " + process.env.REDIS_PORT + ".");
  const client = redis.createClient(process.env.REDIS_PORT, process.env.REDIS_IP);

  const getAsync = promisify(client.get).bind(client);
  const reply = await getAsync("mykey");

  return context
      .status(200)
      .succeed(reply);
}

