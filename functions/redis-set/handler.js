"use strict"

const redis = require("redis");
const { promisify } = require("util");

module.exports = async (event, context) => {
  const mydata = event.body.mydata;

  console.log("Using redis ip " + process.env.REDIS_IP + " and port " + process.env.REDIS_PORT + ".");
  const client = redis.createClient(process.env.REDIS_PORT, process.env.REDIS_IP);

  const setAsync = promisify(client.set).bind(client);
  const reply = await setAsync("mykey", mydata);

  return context
      .status(200)
      .succeed(reply);

  /*client.set('mykey', mydata, (err, reply) => {
    if(err) throw err;
    return context
        .status(200)
        .succeed(reply);
  });*/
}
