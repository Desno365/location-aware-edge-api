'use strict';

/**
 * Returns the location object of the referring area relative to the location represented by ownLocationId.
 * Assumes that ownLocationId is always present in infrastructureJson.
 * @param infrastructureJson the JSON of the infrastructure.
 * @param ownLocationId the location id of the location that is requesting the referring area.
 * @param referringAreaTypeLevel the level of the referring area type.
 * @returns {*|{}} the location id of the referring area.
 */
exports.getLocationObjectOfReferringAreaInInfrastructure = function(infrastructureJson, ownLocationId, referringAreaTypeLevel) {
    const areaTypesIdentifiers = infrastructureJson.areaTypesIdentifiers;
    const hierarchy = infrastructureJson.hierarchy;
    const listOfParents = getListOfParentsForLocationIdInHierarchy(hierarchy, areaTypesIdentifiers, ownLocationId);
    console.log("The list of parents for " + ownLocationId + " is: " + listOfParents + ".");
    const referringAreaId = listOfParents[referringAreaTypeLevel];
    return getLocationObjectInHierarchy(hierarchy, areaTypesIdentifiers, referringAreaId);
}


// ############################################################################
//region Location object of the referring area methods.
// ############################################################################

function getListOfParentsForLocationIdInHierarchy(hierarchy, areaTypesIdentifiers, ownLocationId) {
    const invertedList = getListOfParentsForLocationIdInAreasContainer(hierarchy, areaTypesIdentifiers, 0, ownLocationId);
    invertedList.reverse();
    return invertedList;
}

function getListOfParentsForLocationIdInAreasContainer(areasContainer, areaTypesIdentifiers, level, ownLocationId) {
    // Check if it is an areas container or a locations container (last level).
    if(areaTypesIdentifiers.length > level) {
        // It's an areas container.
        for(const areaName in areasContainer) {
            if(areaName === "main-location") {
                continue;
            }
            if(areaName === ownLocationId) {
                console.log("Own location found in areas container (id: " + areaName + ", level: " + level + ").");
                const listOfParents = [];
                listOfParents.push(areaName);
                return listOfParents;
            } else {
                const resultOfLowerLevel = getListOfParentsForLocationIdInAreasContainer(areasContainer[areaName], areaTypesIdentifiers, level + 1, ownLocationId);
                console.log("Area " + areaName + " has been searched if it contains the own location id " + ownLocationId + ", the result is: " + resultOfLowerLevel + ".");
                if(resultOfLowerLevel !== null) {
                    resultOfLowerLevel.push(areaName);
                    return resultOfLowerLevel;
                }
            }
        }
        return null;
    } else {
        // It's actually a locations container (each field in areasContainer is a location object).
        return getListOfParentsForLocationIdInLocationsContainer(areasContainer, level, ownLocationId);
    }
}

function getListOfParentsForLocationIdInLocationsContainer(locationsContainer, level, ownLocationId) {
    for(const locationName in locationsContainer) {
        if(locationName === ownLocationId) {
            console.log("Own location found in locations container (id: " + locationName + ", level: " + level + ").");
            const listOfParents = [];
            listOfParents.push(locationName);
            return listOfParents;
        }
    }
    return null;
}

function getLocationObjectInHierarchy(hierarchy, areaTypesIdentifiers, locationId) {
    return getLocationObjectInAreasContainer(hierarchy, areaTypesIdentifiers, 0, locationId);
}

function getLocationObjectInAreasContainer(areasContainer, areaTypesIdentifiers, level, locationId) {
    // Check if it is an areas container or a locations container (last level).
    if(areaTypesIdentifiers.length > level) {
        // It's an areas container.
        for(const areaName in areasContainer) {
            if(areaName === "main-location") {
                continue;
            }
            if(areaName === locationId) {
                console.log("Location found in areas container (id: " + areaName + ", level: " + level + ").");
                const locationObject = areasContainer[areaName]["main-location"];
                locationObject.location_id = locationId;
                return locationObject;
            } else {
                const resultOfLowerLevel = getLocationObjectInAreasContainer(areasContainer[areaName], areaTypesIdentifiers, level + 1, locationId);
                console.log("Area " + areaName + " has been searched if it contains the location id " + locationId + ", the result is: " + resultOfLowerLevel + ".");
                if(resultOfLowerLevel !== null) {
                    return resultOfLowerLevel;
                }
            }
        }
        return null;
    } else {
        // It's actually a locations container (each field in areasContainer is a location object).
        return getLocationObjectInLocationsContainer(areasContainer, level, locationId);
    }
}

function getLocationObjectInLocationsContainer(locationsContainer, level, locationId) {
    for(const locationName in locationsContainer) {
        if(locationName === locationId) {
            console.log("Location found in locations container (id: " + locationName + ", level: " + level + ").");
            const locationObject = locationsContainer[locationName];
            locationObject.location_id = locationId;
            return locationObject;
        }
    }
    return null;
}
//endregion
