'use strict'

module.exports = async (event, context) => {
  const result = {
    'body': JSON.stringify(event.body),
    'content-type': event.headers["content-type"],
    'version': process.version
  }

  return context
    .status(200)
    .succeed(result)
}