"use strict";

const redis = require("redis");
const { promisify } = require("util");
const rp = require('request-promise');
const onBoardInfrastructureParser = require("./onBoardInfrastructureParser");

// Constants.
const TTL_MAX_VALUE = 365 * 24 * 60 * 60 * 1000; // 365 days * 24 hours * 60 minutes * 60 seconds * 1000 milliseconds
const TTL_MIN_VALUE = 100; // 100 milliseconds.

// Variables.
let localRedisClient;

exports.withDataDomain = function(dataDomain) {
    const referringAreaType = dataDomain.referringAreaType;
    const ttl = dataDomain.ttl;
    return new EdgeDbClientWithDataDomain(referringAreaType, ttl);
}

exports.get = function(key) {
    return performActionLocally("GET", [key]);
}

let performActionLocally = exports.performActionLocally = function(command, args) {
    createRedisClient();
    switch(command) {
        case "GET":
            const getAsync = promisify(localRedisClient.get).bind(localRedisClient);
            console.log("Executing local GET with args: " + args);
            return getAsync(args);
        case "SET":
            const setAsync = promisify(localRedisClient.set).bind(localRedisClient);
            console.log("Executing local SET with args: " + args);
            return setAsync(args);
        default:
            throw "Command not recognized";
    }
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

function performActionRemotely(gateway, command, args) {
    let options = {
        uri: gateway + "/function/edge-db-data-receiver",
        method: 'POST',
        headers: {
            'User-Agent': 'Request-Promise',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'command': command,
            'args': args,
        }),
    };

    return rp(options);
}

class EdgeDbClientWithDataDomain {
    constructor(referringAreaType, ttl) {
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

        // Initialize variables.
        this.infrastructureJson = JSON.parse(process.env.EDGE_INFRASTRUCTURE);
        this.ownLocationId = process.env.LOCATION_ID;
        this.referringAreaType = referringAreaType;
        this.referringAreaTypeLevel = -1;
        this.referringAreaLocationId = null;
        this.referringAreaLocationObject = null;
        this.ttl = ttl;
        this.shouldForwardWrite = null;

        // Save referringAreaType and check that it is valid.
        const areaTypesIdentifiers = this.infrastructureJson.areaTypesIdentifiers;
        const possibleAreaTypesIdentifiers = areaTypesIdentifiers.concat(["location"]);
        this.referringAreaTypeLevel = possibleAreaTypesIdentifiers.indexOf(referringAreaType);
        if(this.referringAreaTypeLevel === -1) {
            throw "Field referringAreaType is not a valid area type identifier. Valid identifiers for the infrastructure are: " + possibleAreaTypesIdentifiers + ".";
        }

        console.log("Creating EdgeDbClientWithDataDomain having referringAreaType: " + referringAreaType + ", ttl: " + ttl + ".");
        if(referringAreaType === "location") {
            console.log("Writes will be local.");
            this.shouldForwardWrite = false;
        } else {
            this.referringAreaLocationId = onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(this.infrastructureJson, this.ownLocationId, this.referringAreaTypeLevel);
            console.log("Found location id of referring area: " + this.referringAreaLocationId + ".");
            if(this.referringAreaLocationId === this.ownLocationId) {
                console.log("Writes will be local.");
                this.shouldForwardWrite = false;
            } else {
                this.referringAreaLocationObject = onBoardInfrastructureParser.getLocationObject(this.infrastructureJson, this.referringAreaLocationId);
                console.log("Writes will be local and remote (forwarded to " + this.referringAreaLocationObject.openfaas_gateway + ").");
                this.shouldForwardWrite = true;
            }
        }
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
        const localResponse = await performActionLocally("SET", args);
        console.log("Executed local SET.");

        // Propagate action and return.
        if(localResponse === 'OK' && this.shouldForwardWrite) {
            const remoteResponse = await performActionRemotely(this.referringAreaLocationObject.openfaas_gateway, "SET", args);
            console.log("Executed remote SET. Response: " + remoteResponse);
            return 'OK';
        } else {
            return localResponse;
        }
    }
}
