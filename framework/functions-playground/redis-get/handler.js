"use strict";

const redis = require("redis");
const { promisify } = require("util");

module.exports = async (event, context) => {
  console.log("Using redis host \"" + process.env.REDIS_HOST + "\" and port \"" + process.env.REDIS_PORT + "\".");
  const client = redis.createClient({
    host: process.env.REDIS_HOST,
    port: process.env.REDIS_PORT,
    password: process.env.REDIS_PASSWORD
  });

  const getAsync = promisify(client.get).bind(client);
  const reply = await getAsync("mykey");

  return context
      .status(200)
      .succeed(reply);
}

