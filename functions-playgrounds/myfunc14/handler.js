'use strict'

let myVar = 0;

module.exports = async (event, context) => {
  myVar++;

  const result = {
    'body': JSON.stringify(event.body),
    'content-type': event.headers["content-type"],
    'version': myVar
  };

  return context
    .status(200)
    .succeed(result);
}
