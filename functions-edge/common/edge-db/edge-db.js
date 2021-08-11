"use strict";

const redis = require("redis");
const { promisify } = require("util");

// Constants.
const TTL_MAX_VALUE = 365 * 24 * 60 * 60 * 1000; // 365 days * 24 hours * 60 minutes * 60 seconds * 1000 milliseconds
const TTL_MIN_VALUE = 100; // 100 milliseconds.

// Variables.
let localRedisClient;

exports.withDataDomain = function(dataDomain) {
    createRedisClient();
    const referringAreaType = dataDomain.referringAreaType;
    const ttl = dataDomain.ttl;
    return new EdgeDbClientWithDataDomain(referringAreaType, ttl);
}

exports.get = function (key) {
    createRedisClient();
    const getAsync = promisify(localRedisClient.get).bind(localRedisClient);
    return getAsync(key);
}

function createRedisClient() {
    if(!localRedisClient) {
        console.log("Creating redis client, using host \"" + process.env.REDIS_HOST + "\" and port \"" + process.env.REDIS_PORT + "\".");
        localRedisClient = redis.createClient({
            host: process.env.REDIS_HOST,
            port: process.env.REDIS_PORT,
            password: process.env.REDIS_PASSWORD
        });
    }
}

class EdgeDbClientWithDataDomain {
    constructor(referringAreaType, ttl) {
        this.referringAreaType = referringAreaType;
        this.ttl = ttl;
        this.infrastructureJson = JSON.parse(process.env.EDGE_INFRASTRUCTURE);

        const areaTypesIdentifiers = this.infrastructureJson.areaTypesIdentifiers;
        const possibleAreaTypesIdentifiers = areaTypesIdentifiers.concat(["location"]);
        this.referringAreaTypeLevel = possibleAreaTypesIdentifiers.indexOf(referringAreaType);

        // Check correctness.
        if(!referringAreaType) {
            throw "Field referringAreaType not set.";
        }
        if(!(typeof referringAreaType === 'string' || referringAreaType instanceof String)) {
            throw "Field referringAreaType is not a string.";
        }
        if(!ttl) {
            throw "Field ttl not set.";
        }
        if(!Number.isInteger(ttl)) {
            throw "Field ttl is not an integer.";
        }
        if(ttl > TTL_MAX_VALUE) {
            throw "Field ttl is too big. It must be lower than " + TTL_MAX_VALUE + ".";
        }
        if(ttl < TTL_MIN_VALUE) {
            throw "Field ttl is too small. It must be bigger than " + TTL_MIN_VALUE + ".";
        }

        // Check that referringAreaType is valid.
        if(referringAreaTypeLevel === -1) {
            throw "Field referringAreaType is not a valid area type identifier. Valid identifiers for the infrastructure are: " + possibleAreaTypesIdentifiers + ".";
        }

        console.log("Creating EdgeDbClientWithDataDomain having referringAreaType: " + referringAreaType + ", ttl: " + ttl + ".");
    }

    async set(key, data, onlySetIfKeyDoesNotAlreadyExist, onlySetIfKeyAlreadyExist) {
        if(onlySetIfKeyDoesNotAlreadyExist === true && onlySetIfKeyAlreadyExist === true) {
            throw "Only one option between onlySetIfKeyDoesNotAlreadyExist and onlySetIfKeyAlreadyExist can be enabled.";
        }

        // Prepare arguments.
        const args = [key, data, "PX", this.ttl]; // https://redis.io/commands/set
        if(onlySetIfKeyDoesNotAlreadyExist === true)
            args.push("NX");
        if(onlySetIfKeyAlreadyExist === true)
            args.push("XX");

        // Execute action locally.
        const setAsync = promisify(localRedisClient.set).bind(localRedisClient);
        const reply = await setAsync(args);
        console.log("Executed local SET with args: " + args);

        // Propagate action and return.
        if(reply === 'OK' && this.referringAreaType !== "location") {
            // TODO: send to other db depending on data domain.
            console.log("MISSING IMPLEMENTATION.");
            return 'MISSING_IMPLEMENTATION';
        } else {
            return reply;
        }
    }
}