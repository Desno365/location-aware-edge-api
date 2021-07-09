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

exports.getAllLocations = function(infrastructureJson) {
    const areaTypesIdentifiers = infrastructureJson.areaTypesIdentifiers;
    const hierarchy = infrastructureJson.hierarchy;
    return getListOfLocationsInHierarchyObject(hierarchy, areaTypesIdentifiers);
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
//region Get all locations methods.
// ############################################################################

function getListOfLocationsInHierarchyObject(hierarchy, areaTypesIdentifiers) {
    return getListOfLocationsInAreasContainer(hierarchy, areaTypesIdentifiers, 0);
}

function getListOfLocationsInAreasContainer(areasContainer, areaTypesIdentifiers, level) {
    // Check if it is an areas container or a locations container (last level).
    if(areaTypesIdentifiers.length > level) {
        // It's an areas container.
        let listOfLocations = [];
        for(const area in areasContainer) {
            const subListOfLocations = getListOfLocationsInAreasContainer(areasContainer[area], areaTypesIdentifiers, level + 1);
            console.log("Area " + area + " has " + subListOfLocations.length + " locations inside.");
            listOfLocations = listOfLocations.concat(subListOfLocations);
        }
        return listOfLocations;
    } else {
        // It's actually a locations container (each field in areasContainer is a location object).
        return getListOfLocationsInLocationsContainer(areasContainer);
    }
}

function getListOfLocationsInLocationsContainer(locationsContainer) {
    let listOfLocations = [];
    for(const location in locationsContainer) {
        const locationObject = locationsContainer[location];
        console.log("Location " + location + " has been added to the list.");
        listOfLocations.push(locationObject);
    }
    return listOfLocations;
}
//endregion
