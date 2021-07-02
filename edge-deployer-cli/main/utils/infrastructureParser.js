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

let areaNames;

function isHierarchyObjectCorrect(hierarchy, areaTypesIdentifiers) {
    areaNames = [];
    return isAreasContainerCorrect(hierarchy, areaTypesIdentifiers, 0);
}

function isAreasContainerCorrect(areasContainer, areaTypesIdentifiers, level) {
    // Check if it is an areas container or a locations container (last level).
    if(areaTypesIdentifiers.length > level) {
        // It's an areas container.
        const currentAreaTypeIdentifier = areaTypesIdentifiers[level];
        for(const area in areasContainer) {
            console.log("Currently analyzing area: " + area + ".");
            if(!canBeValidArea(area, areaTypesIdentifiers)) {
                console.log(chalk.red("Error: area with name \"" + area + "\" of type \"" + currentAreaTypeIdentifier + "\" is not a valid name."));
                return false;
            }
            if(!isAreasContainerCorrect(areasContainer[area], areaTypesIdentifiers, level + 1)) {
                console.log(chalk.red("Error: area with name \"" + area + "\" of type \"" + currentAreaTypeIdentifier + "\" is not a valid area."));
                return false;
            }
            console.log(chalk.green("Area \"" + area + "\" is correct."));
        }
        return true;
    } else {
        // It's actually a locations container (each field in areasContainer is a location object).
        return isLocationsContainerCorrect(areasContainer, areaTypesIdentifiers);
    }
}

function isLocationsContainerCorrect(locationsContainer, areaTypesIdentifiers) {
    for(const location in locationsContainer) {
        console.log("Currently analyzing location: " + location + ".");
        if(!canBeValidArea(location, areaTypesIdentifiers)) {
            console.log(chalk.red("Error: location with name \"" + location + "\" is not a valid name."));
            return false;
        }
        if(!canBeValidLocation(locationsContainer[location])) {
            console.log(chalk.red("Error: location with name \"" + location + "\" is not a valid location (the location must contain an ip, a port and a password)."));
            return false;
        }
        console.log(chalk.green("Location \"" + location + "\" is correct."));
    }
    return true;
}

function isAUniqueAreaName(areaNameString) {
    const isUnique = areaNames.indexOf(areaNameString) === -1; // It is unique if the array of names does not contain the name.
    areaNames.push(areaNameString);
    return isUnique;
}

function canBeValidArea(areaNameString, areaTypesIdentifiers) {
    if(!isAUniqueAreaName(areaNameString)) {
        console.log(chalk.red("Error: area names must be unique. There are more than one area with name \"" + areaNameString + "\"."));
        return false;
    } else if(!canBeValidAreaName(areaNameString, areaTypesIdentifiers)) {
        console.log(chalk.red("Error: area with name \"" + areaNameString + "\" is not a valid name."));
        return false;
    } else {
        return true;
    }
}

function canBeValidAreaType(areaTypeString) {
    return (typeof areaTypeString === 'string' || areaTypeString instanceof String)
        && areaTypeString !== 'ip' && areaTypeString !== 'port' && areaTypeString !== 'password';
}

function canBeValidAreaName(areaNameString, areaTypesIdentifiersArray) {
    return (typeof areaNameString === 'string' || areaNameString instanceof String)
        && areaNameString !== 'ip' && areaNameString !== 'port' && areaNameString !== 'password'
        && areaTypesIdentifiersArray.every((areaType) => areaType !== areaNameString);
}

function canBeValidLocation(locationObject) {
    return locationObject.ip && locationObject.port && locationObject.password;
}