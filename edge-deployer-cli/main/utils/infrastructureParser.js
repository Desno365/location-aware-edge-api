'use strict';

const chalk = require('chalk');

exports.isInfrastructureJsonCorrect = function(infrastructureJson) {
    const areaTypesIdentifiers = infrastructureJson.areaTypesIdentifiers;
    const hierarchy = infrastructureJson.hierarchy;
    if(!hierarchy) {
        console.log(chalk.red("Error: field hierarchy not specified."));
        return false;
    } else if(!areaTypesIdentifiers) {
        console.log(chalk.red("Error: field areaTypesIdentifiers not specified."));
        return false;
    } else if(!Array.isArray(areaTypesIdentifiers)) {
        console.log(chalk.red("Error: field areaTypesIdentifiers is not an array."));
        return false;
    } else if(!areaTypesIdentifiers.every((areaType) => canBeValidAreaType(areaType))) {
        console.log(chalk.red("Error: area types must be string and different than reserved keywords."));
        return false;
    } else {
        return isHierarchyObjectCorrect(hierarchy, areaTypesIdentifiers);
    }
}

exports.isDeploymentInputCorrect = function(infrastructureJson, inEvery, inAreas, exceptIn) {
    const areaTypesIdentifiers = infrastructureJson.areaTypesIdentifiers;

    // Check that inEvery field is valid.
    const possibleAreaTypesIdentifiers = areaTypesIdentifiers.concat(["location"]);
    if(!(possibleAreaTypesIdentifiers.includes(inEvery))) {
        console.log(chalk.red("Error: --inEvery is not a valid area type identifier. Valid identifiers for the infrastructure are: " + possibleAreaTypesIdentifiers + "."));
        return false;
    }

    // Check that inAreas field is valid.
    if(inAreas !== null && inAreas !== undefined) {
        if(!Array.isArray(inAreas)) {
            console.log(chalk.red("Error: field inAreas is not an array."));
            return false;
        }

        // The areas specified in inAreas must have an area type bigger or equal than the area type specified in inEvery.
        const inEveryLevel = possibleAreaTypesIdentifiers.indexOf(inEvery);
        for(const areaName of inAreas) {
            const areaLevel = getAreaLevel(infrastructureJson, areaName);
            if(areaLevel === null) {
                console.log(chalk.red("Error: --inAreas contains an area that does not exist in the infrastructure. Area: " + areaName + "."));
                return false;
            }
            if(inEveryLevel < areaLevel) {
                console.log(chalk.red("Error: the areas specified in --inAreas must have an area type bigger or equal than the area type specified in --inEvery."));
                console.log(chalk.red("This error has been found while analyzing area: " + areaName + "."));
                return false;
            }
        }
    }

    // Check that exceptIn field is valid.
    if(exceptIn !== null && exceptIn !== undefined) {
        if(!Array.isArray(exceptIn)) {
            console.log(chalk.red("Error: field exceptIn is not an array."));
            return false;
        }

        for(const areaName of exceptIn) {
            const areaLevel = getAreaLevel(infrastructureJson, areaName);
            if(areaLevel === null) {
                console.log(chalk.red("Error: --exceptIn contains an area that does not exist in the infrastructure. Area: " + areaName + "."));
                return false;
            }
        }
    }

    // All correct.
    return true;
}

let getAreaLevel = exports.getAreaLevel = function(infrastructureJson, areaNameToBeChecked) {
    const areaTypesIdentifiers = infrastructureJson.areaTypesIdentifiers;
    const hierarchy = infrastructureJson.hierarchy;
    return checkIfAreaIsInHierarchyAndGetLevel(hierarchy, areaTypesIdentifiers, areaNameToBeChecked);
}

exports.getAllLocations = function(infrastructureJson, inEvery, inAreas, exceptIn) {
    const areaTypesIdentifiers = infrastructureJson.areaTypesIdentifiers;
    const hierarchy = infrastructureJson.hierarchy;
    return getListOfLocationsInHierarchyObject(hierarchy, areaTypesIdentifiers, inEvery, inAreas, exceptIn);
}


// ############################################################################
//region Check correctness methods.
// ############################################################################

let areaNames; // Used to check if area name is unique.
function isHierarchyObjectCorrect(hierarchy, areaTypesIdentifiers) {
    areaNames = [];
    return isAreasContainerCorrect(hierarchy, areaTypesIdentifiers, 0);
}

function isAreasContainerCorrect(areasContainer, areaTypesIdentifiers, level) {
    // Check if it is an areas container or a locations container (last level).
    if(areaTypesIdentifiers.length > level) {
        // It's an areas container.
        const currentAreaTypeIdentifier = areaTypesIdentifiers[level];
        for(const areaName in areasContainer) {
            console.log("Currently analyzing area: " + areaName + ".");
            if(!canBeValidArea(areaName, areaTypesIdentifiers)) {
                console.log(chalk.red("Error: area with name \"" + areaName + "\" of type \"" + currentAreaTypeIdentifier + "\" is not a valid name."));
                return false;
            }
            if(!isAreasContainerCorrect(areasContainer[areaName], areaTypesIdentifiers, level + 1)) {
                console.log(chalk.red("Error: area with name \"" + areaName + "\" of type \"" + currentAreaTypeIdentifier + "\" is not a valid area."));
                return false;
            }
            console.log(chalk.green("Area \"" + areaName + "\" is correct."));
        }
        return true;
    } else {
        // It's actually a locations container (each field in areasContainer is a location object).
        return isLocationsContainerCorrect(areasContainer, areaTypesIdentifiers);
    }
}

function isLocationsContainerCorrect(locationsContainer, areaTypesIdentifiers) {
    for(const locationName in locationsContainer) {
        console.log("Currently analyzing location: " + locationName + ".");
        if(!canBeValidArea(locationName, areaTypesIdentifiers)) {
            console.log(chalk.red("Error: location with name \"" + locationName + "\" is not a valid name."));
            return false;
        }
        if(!canBeValidLocation(locationsContainer[locationName])) {
            console.log(chalk.red("Error: location with name \"" + locationName + "\" is not a valid location (the location must contain an ip, a port and a password)."));
            return false;
        }
        console.log(chalk.green("Location \"" + locationName + "\" is correct."));
    }
    return true;
}

function isAUniqueAreaName(areaName) {
    const isUnique = areaNames.indexOf(areaName) === -1; // It is unique if the array of names does not contain the name.
    areaNames.push(areaName);
    return isUnique;
}

function canBeValidArea(areaName, areaTypesIdentifiers) {
    if(!isAUniqueAreaName(areaName)) {
        console.log(chalk.red("Error: area names must be unique. There are more than one area with name \"" + areaName + "\"."));
        return false;
    } else if(!canBeValidAreaName(areaName, areaTypesIdentifiers)) {
        console.log(chalk.red("Error: area with name \"" + areaName + "\" is not a valid name."));
        return false;
    } else {
        return true;
    }
}

function canBeValidAreaType(areaType) {
    return (typeof areaType === 'string' || areaType instanceof String)
        && areaType !== 'ip' && areaType !== 'port' && areaType !== 'password';
}

function canBeValidAreaName(areaName, areaTypesIdentifiers) {
    return (typeof areaName === 'string' || areaName instanceof String)
        && areaName !== 'ip' && areaName !== 'port' && areaName !== 'password'
        && areaTypesIdentifiers.every((areaType) => areaType !== areaName);
}

function canBeValidLocation(location) {
    return location.ip && location.port && location.password;
}
//endregion


// ############################################################################
//region Get level of area methods.
// ############################################################################

function checkIfAreaIsInHierarchyAndGetLevel(hierarchy, areaTypesIdentifiers, areaNameToBeChecked) {
    return checkIfAreaIsInAreasContainerAndGetLevel(hierarchy, areaTypesIdentifiers, 0, areaNameToBeChecked);
}

function checkIfAreaIsInAreasContainerAndGetLevel(areasContainer, areaTypesIdentifiers, level, areaNameToBeChecked) {
    // Check if it is an areas container or a locations container (last level).
    if(areaTypesIdentifiers.length > level) {
        // It's an areas container.
        for(const areaName in areasContainer) {
            if(areaName === areaNameToBeChecked) {
                console.log("Area " + areaName + " is the area searched amd it has a level of " + level + ".");
                return level;
            }
            const resultOfLowerLevel = checkIfAreaIsInAreasContainerAndGetLevel(areasContainer[areaName], areaTypesIdentifiers, level + 1, areaNameToBeChecked);
            console.log("Area " + areaName + " has been searched if it contains the area called " + areaNameToBeChecked + ", the result is: " + resultOfLowerLevel + ".");
            if(resultOfLowerLevel !== null)
                return resultOfLowerLevel;
        }
        return null;
    } else {
        // It's actually a locations container (each field in areasContainer is a location object).
        const resultOfLocationsLevel = checkIfAreaIsInLocationsContainerAndGetLevel(areasContainer, level, areaNameToBeChecked);
        console.log("A locations container has been searched if it contains the area called " + areaNameToBeChecked + ", the result is: " + resultOfLocationsLevel + ".");
        return resultOfLocationsLevel;
    }
}

function checkIfAreaIsInLocationsContainerAndGetLevel(locationsContainer, level, areaNameToBeChecked) {
    for(const locationName in locationsContainer) {
        if(locationName === areaNameToBeChecked) {
            console.log("Location " + locationName + " is the area searched and it has a level of " + level + ".");
            return level;
        }
    }
    return null;
}
//endregion


// ############################################################################
//region Get all locations methods.
// ############################################################################

function getListOfLocationsInHierarchyObject(hierarchy, areaTypesIdentifiers, inEvery, inAreas, exceptIn) {
    let listOfLocations = [];
    const subListOfLocations = getListOfLocationsInAreasContainer(hierarchy, areaTypesIdentifiers, inEvery, inAreas, exceptIn, [], 0);
    listOfLocations = listOfLocations.concat(subListOfLocations);
    return listOfLocations;
}

function getListOfLocationsInAreasContainer(areasContainer, areaTypesIdentifiers, inEvery, inAreas, exceptIn, listOfParents, level) {
    // Check if it is an areas container or a locations container (last level).
    if(areaTypesIdentifiers.length > level) {
        // It's an areas container.
        let listOfLocations = [];
        for(const areaName in areasContainer) {
            const subListOfLocations = getListOfLocationsInAreasContainer(areasContainer[areaName], areaTypesIdentifiers, inEvery, inAreas, exceptIn, listOfParents.concat(areaName), level + 1);
            console.log("Area " + areaName + " has " + subListOfLocations.length + " included locations inside.");
            listOfLocations = listOfLocations.concat(subListOfLocations);
        }
        return listOfLocations;
    } else {
        // It's actually a locations container (each field in areasContainer is a location object).
        return getListOfLocationsInLocationsContainer(areasContainer, inEvery, inAreas, exceptIn, listOfParents);
    }
}

function getListOfLocationsInLocationsContainer(locationsContainer, inEvery, inAreas, exceptIn, listOfParents) {
    let listOfLocations = [];
    for(const locationName in locationsContainer) {
        const listOfLocationAndItsParents = listOfParents.concat(locationName);
        if(shouldLocationBeIncluded(listOfLocationAndItsParents, inAreas) && !shouldLocationBeExcluded(listOfLocationAndItsParents, exceptIn)) {
            const locationObject = locationsContainer[locationName];
            console.log("Location " + locationName + " has been added to the list.");
            listOfLocations.push(locationObject);
        }
    }
    return listOfLocations;
}

function shouldLocationBeIncluded(listOfLocationAndItsParents, inAreas) {
    if(inAreas === null || inAreas === undefined) {
        return true;
    }
    for(const areaName of listOfLocationAndItsParents) {
        if(inAreas.includes(areaName)) {
            return true;
        }
    }
    return false;
}

function shouldLocationBeExcluded(listOfLocationAndItsParents, exceptIn) {
    if(exceptIn === null || exceptIn === undefined) {
        return false;
    }
    for(const areaName of listOfLocationAndItsParents) {
        if(exceptIn.includes(areaName)) {
            return true;
        }
    }
    return false;
}

//endregion
