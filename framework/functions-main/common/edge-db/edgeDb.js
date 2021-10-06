"use strict";

const { promisify } = require("util");
const onBoardInfrastructureParser = require("./onBoardInfrastructureParser");
const savingTypeEnum = require("./savingTypeEnum");

// Constants.
const TTL_MAX_VALUE = 365 * 24 * 60 * 60 * 1000; // 365 days * 24 hours * 60 minutes * 60 seconds * 1000 milliseconds
const TTL_MIN_VALUE = 100; // 100 milliseconds.

// Variables.
let localRedisClient;

exports.withDataDomain = function(dataDomain) {
    return new EdgeDbClientWithDataDomain(dataDomain.referringAreaType, dataDomain.ttl, dataDomain.saveAlsoInIntermediateLevels);
}

exports.get = function(key) {
    return performActionLocally("GET", [key]); // https://redis.io/commands/get
}

exports.getList = async function(key) {
    const currentTimeMS = getCurrentTimeInMilliseconds();

    // Expire items.
    await performActionLocally("ZREMRANGEBYSCORE", [key, "0", currentTimeMS]); // https://redis.io/commands/zremrangebyscore

    // Return not expired items.
    const list = await performActionLocally("ZRANGEBYSCORE", [key, currentTimeMS, "+inf"]); // https://redis.io/commands/zrangebyscore

    // Remove timestamp from value.
    for(let i = 0; i < list.length; i++) {
        list[i] = list[i].substring(list[i].indexOf(":") + 1);
    }

    return list;
}

let performActionLocally = exports.performActionLocally = async function(command, args) {
    createRedisClient();
    let asyncCommand;
    switch(command) {
        case "GET":
            asyncCommand = promisify(localRedisClient.get).bind(localRedisClient);
            break;
        case "SET":
            asyncCommand = promisify(localRedisClient.set).bind(localRedisClient);
            break;
        case "ZADD":
            asyncCommand = promisify(localRedisClient.zadd).bind(localRedisClient);
            break;
        case "ZRANGEBYSCORE":
            asyncCommand = promisify(localRedisClient.zrangebyscore).bind(localRedisClient);
            break;
        case "ZREMRANGEBYSCORE":
            asyncCommand = promisify(localRedisClient.zremrangebyscore).bind(localRedisClient);
            break;
        default:
            throw "Command not recognized";
    }

    console.log("Executing local " + command + " with args: " + args + ".");
    const response = String(await asyncCommand(args));
    console.log("Finished executing local " + command + ". Response: " + response);

    return response;
}

function createRedisClient() {
    if(!localRedisClient) {
        console.log("Creating redis client, using host \"" + process.env.REDIS_HOST + "\" and port \"" + process.env.REDIS_PORT + "\".");
        localRedisClient = require("redis").createClient({
            host: process.env.REDIS_HOST,
            port: process.env.REDIS_PORT,
            password: process.env.REDIS_PASSWORD
        });
    }
}

async function performActionRemotely(gateway, command, args) {
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

    console.log("Executing remote " + command + " with args: " + args + ".");
    const rp = require('request-promise');
    const response = String(await rp(options));
    console.log("Finished executing remote " + command + ". Response: " + response);

    return response;
}

function getCurrentTimeInMilliseconds() {
    const now = new Date();
    return now.getTime();
}

class EdgeDbClientWithDataDomain {
    constructor(referringAreaType, ttl, saveAlsoInIntermediateLevels) {
        // Check correctness.
        if(!(typeof referringAreaType === 'string' || referringAreaType instanceof String)) {
            throw "Field referringAreaType is not a string.";
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
        if(referringAreaType !== "location" && process.env.EDGE_DEPLOYMENT_IN_EVERY !== referringAreaType) {
            // If referringAreaType is different than location and the deployment area level is different than the referringAreaType:
            // then the user must also define if enabling saving also in intermediate locations.
            if(!(saveAlsoInIntermediateLevels === true || saveAlsoInIntermediateLevels === false)) {
                throw "Field saveAlsoInIntermediateLevels must be specified and must be a boolean.";
            }
        }

        // Initialize variables.
        this.infrastructureJson = JSON.parse(process.env.EDGE_INFRASTRUCTURE);
        this.ownLocationId = process.env.LOCATION_ID;
        this.ownAreaTypeLevel = null;
        this.referringAreaType = referringAreaType;
        this.referringAreaTypeLevel = -1;
        this.ttl = ttl;
        this.saveAlsoInIntermediateLevels = saveAlsoInIntermediateLevels;
        this.savingLocationsList = [];
        this.savingType = null;

        // Save referringAreaType and check that it is valid.
        const areaTypesIdentifiers = this.infrastructureJson.areaTypesIdentifiers;
        const possibleAreaTypesIdentifiers = areaTypesIdentifiers.concat(["location"]);
        this.ownAreaTypeLevel = possibleAreaTypesIdentifiers.indexOf(process.env.EDGE_DEPLOYMENT_IN_EVERY);
        this.referringAreaTypeLevel = possibleAreaTypesIdentifiers.indexOf(referringAreaType);
        if(this.referringAreaTypeLevel === -1) {
            throw "Field referringAreaType is not a valid area type identifier. Valid identifiers for the infrastructure are: " + possibleAreaTypesIdentifiers + ".";
        }

        console.log("Creating EdgeDbClientWithDataDomain having referringAreaType: " + referringAreaType + ", ttl: " + ttl + ", saveAlsoInIntermediateLevels: " + saveAlsoInIntermediateLevels + ".");

        if(referringAreaType === "location" || process.env.EDGE_DEPLOYMENT_IN_EVERY === referringAreaType) {
            console.log("Writes will be local.");
            this.savingType = savingTypeEnum.ONLY_LOCAL;
        } else {
            if(this.saveAlsoInIntermediateLevels) {
                console.log("Writes will be saved also in intermediate levels.");
                this.savingType = savingTypeEnum.SAVE_ALSO_IN_INTERMEDIATE_LEVELS;
                for(let level = this.referringAreaTypeLevel; level <= this.ownAreaTypeLevel; level++) {
                    const locationObject = onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(this.infrastructureJson, this.ownLocationId, level);
                    if(locationObject.location_id !== this.ownLocationId) {
                        this.savingLocationsList.push(locationObject);
                    }
                }
            } else {
                const referringAreaLocationObject = onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(this.infrastructureJson, this.ownLocationId, this.referringAreaTypeLevel);
                console.log("Location id of referring area: " + referringAreaLocationObject.location_id + ".");
                if(referringAreaLocationObject.location_id === this.ownLocationId) {
                    console.log("The single referring area is the current location. So writes will be only local");
                    this.savingType = savingTypeEnum.ONLY_LOCAL;
                } else {
                    this.savingLocationsList.push(referringAreaLocationObject);
                    console.log("Writes will be remote to a single location (forwarded to " + referringAreaLocationObject.openfaas_gateway + ").");
                    this.savingType = savingTypeEnum.SINGLE_REMOTE;
                }
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

        // Write.
        return this.performWrite("SET", args);
    }

    async addToList(key, data, onlySetIfKeyDoesNotAlreadyExist, onlySetIfKeyAlreadyExist) {
        if(onlySetIfKeyDoesNotAlreadyExist === true && onlySetIfKeyAlreadyExist === true) {
            throw "Only one option between onlySetIfKeyDoesNotAlreadyExist and onlySetIfKeyAlreadyExist can be enabled.";
        }

        // Prepare arguments.
        const score = getCurrentTimeInMilliseconds() + this.ttl; // The expiration is used as score.
        const args = []; // https://redis.io/commands/zadd
        args.push(key);
        if(onlySetIfKeyDoesNotAlreadyExist === true)
            args.push("NX");
        if(onlySetIfKeyAlreadyExist === true)
            args.push("XX");
        args.push(score);
        args.push(score + ":" + data);

        // Write.
        return this.performWrite("ZADD", args);
    }

    performWrite(command, args) {
        if(this.savingType === savingTypeEnum.ONLY_LOCAL) { // Only local write.
            return performActionLocally(command, args);
        } else if(this.savingType === savingTypeEnum.SINGLE_REMOTE) { // Single remote saving.
            return performActionRemotely(this.savingLocationsList[0].openfaas_gateway, command, args);
        } else if(this.savingType === savingTypeEnum.SAVE_ALSO_IN_INTERMEDIATE_LEVELS) { // Remote write + intermediate.
            const listOfPromises = [];
            listOfPromises.push(performActionLocally(command, args));
            for(const locationObject of this.savingLocationsList) {
                listOfPromises.push(performActionRemotely(locationObject.openfaas_gateway, command, args));
            }
            return Promise.all(listOfPromises);
        } else {
            throw "Unrecognized savingType";
        }
    }
}
