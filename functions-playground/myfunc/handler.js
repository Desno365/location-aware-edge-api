"use strict";

module.exports = async (context, callback) => {
    return {status: process.version};
}
