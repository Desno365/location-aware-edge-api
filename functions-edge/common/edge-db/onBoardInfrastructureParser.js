'use strict';

/**
 * Returns the location id of the referring area relative to the location represented by ownLocationId.
 * Assumes that ownLocationId is always present in infrastructureJson.
 * @param infrastructureJson the JSON of the infrastructure.
 * @param ownLocationId the location id of the location that is requesting the referring area.
 * @param referringAreaTypeLevel the level of the referring area type.
 * @returns {*|{}} the location id of the referring area.
 */
exports.getLocationIdOfReferringAreaInInfrastructure = function(infrastructureJson, ownLocationId, referringAreaTypeLevel) {
    const areaTypesIdentifiers = infrastructureJson.areaTypesIdentifiers;
    const hierarchy = infrastructureJson.hierarchy;
    return getLocationIdOfReferringAreaInHierarchy(hierarchy, areaTypesIdentifiers, ownLocationId, referringAreaTypeLevel);
}

exports.getLocationObject = function(infrastructureJson, locationIdToBeChecked) {
    const areaTypesIdentifiers = infrastructureJson.areaTypesIdentifiers;
    const hierarchy = infrastructureJson.hierarchy;
    return getLocationObjectInHierarchy(hierarchy, areaTypesIdentifiers, locationIdToBeChecked);
}


// ############################################################################
//region Location id of the referring area methods.
// ############################################################################

function getLocationIdOfReferringAreaInHierarchy(hierarchy, areaTypesIdentifiers, ownLocationId, referringAreaTypeLevel) {
    return getLocationIdOfReferringAreaInAreasContainer(hierarchy, areaTypesIdentifiers, 0, ownLocationId, referringAreaTypeLevel);
}

function getLocationIdOfReferringAreaInAreasContainer(areasContainer, areaTypesIdentifiers, level, ownLocationId, referringAreaTypeLevel) {
    // Check if it is an areas container or a locations container (last level).
    if(areaTypesIdentifiers.length > level) {
        // It's an areas container.
        for(const areaName in areasContainer) {
            if(areaName === "main-location") {
                continue;
            }
            const resultOfLowerLevel = getLocationIdOfReferringAreaInAreasContainer(areasContainer[areaName], areaTypesIdentifiers, level + 1, ownLocationId, referringAreaTypeLevel);
            console.log("Area " + areaName + " has been searched if it contains the own location id " + ownLocationId + ", the result is: " + resultOfLowerLevel + ".");
            if(resultOfLowerLevel !== null) {
                if(referringAreaTypeLevel === level - 1) {
                    const mainLocationData = areasContainer["main-location"];
                    console.log("Found the correct location id of the referring area type: " + mainLocationData + ".");
                    return mainLocationData;
                } else {
                    return resultOfLowerLevel;
                }
            }
        }
        return null;
    } else {
        // It's actually a locations container (each field in areasContainer is a location object).
        return checkIfOwnLocationIsInLocationsContainer(areasContainer, level, ownLocationId);
    }
}

function checkIfOwnLocationIsInLocationsContainer(locationsContainer, level, ownLocationId) {
    for(const locationName in locationsContainer) {
        if(locationName === "main-location") {
            continue;
        }
        if(locationName === ownLocationId) {
            console.log("Own location found (id: " + locationName + ", level: " + level + ").");
            const mainLocationData = locationsContainer["main-location"];
            console.log("Since the own location has been found in the locations container we are returning the main-location of it that is " + mainLocationData + " (may be overwritten later).");
            return mainLocationData;
        }
    }
    return null;
}
//endregion


// ############################################################################
//region Get location object methods.
// ############################################################################

function getLocationObjectInHierarchy(hierarchy, areaTypesIdentifiers, locationIdToBeChecked) {
    return getLocationObjectInAreasContainer(hierarchy, areaTypesIdentifiers, 0, locationIdToBeChecked);
}

function getLocationObjectInAreasContainer(areasContainer, areaTypesIdentifiers, level, locationIdToBeChecked) {
    // Check if it is an areas container or a locations container (last level).
    if(areaTypesIdentifiers.length > level) {
        // It's an areas container.
        for(const areaName in areasContainer) {
            if(areaName === "main-location") {
                continue;
            }
            const resultOfLowerLevel = getLocationObjectInAreasContainer(areasContainer[areaName], areaTypesIdentifiers, level + 1, locationIdToBeChecked);
            console.log("Area " + areaName + " has been searched if it contains the location " + locationIdToBeChecked + ", result: " + (resultOfLowerLevel !== null) + ".");
            if(resultOfLowerLevel !== null)
                return resultOfLowerLevel;
        }
        return null;
    } else {
        // It's actually a locations container (each field in areasContainer is a location object).
        const resultOfLocationsLevel = getLocationObjectInLocationsContainer(areasContainer, level, locationIdToBeChecked);
        console.log("A locations container has been searched if it contains the location " + locationIdToBeChecked + ", result: " + (resultOfLocationsLevel !== null)+ ".");
        return resultOfLocationsLevel;
    }
}

function getLocationObjectInLocationsContainer(locationsContainer, level, locationIdToBeChecked) {
    for(const locationName in locationsContainer) {
        if(locationName === "main-location") {
            continue;
        }
        if(locationName === locationIdToBeChecked) {
            const locationObject = locationsContainer[locationName];
            locationObject.location_id = locationName;
            console.log("Location " + locationName + " is the location searched and it has a level of " + level + ".");
            return locationObject;
        }
    }
    return null;
}
//endregion
