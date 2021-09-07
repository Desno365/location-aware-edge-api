/* eslint-disable promise/no-nesting */
'use strict';

// Dependencies
const chai = require('chai');
const assert = chai.assert;
const fs = require('fs');
const infrastructureParser = require('../main/utils/infrastructureParser');

describe('infrastructureParser', () => {

  describe('isInfrastructureJsonCorrect', () => {

    it('Simple infrastructure without hierarchy', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-without-hierarchy.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('Simple infrastructure without areaTypesIdentifiers', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-without-areaTypesIdentifiers.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('Simple infrastructure with areaTypesIdentifiers not an array', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-with-areaTypesIdentifiers-not-array.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('Simple infrastructure with invalid area type', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-with-invalid-area-type.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('Simple infrastructure with repeating area name', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-with-repeating-area-name.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('Simple infrastructure with invalid area name', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-with-invalid-area-name.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('Simple infrastructure with invalid location name', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-with-invalid-location-name.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('Simple infrastructure with invalid main-location in areas container', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-with-invalid-main-location-in-areas-container.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('Simple infrastructure with invalid main-location in locations container', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-with-invalid-main-location-in-locations-container.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('Simple infrastructure without main-location in areas container', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-without-main-location-in-areas-container.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('Simple infrastructure without main-location in locations container', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-without-main-location-in-locations-container.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('One level infrastructure with invalid location object', () => {
      const infrastructurePath = "./test/test-infrastructures/one-level-infrastructure-with-invalid-location-object.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), false);
    });

    it('Correct infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
    });

    it('Correct one level infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/one-level-infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
    });

    it('Correct simple infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
    });

  });

  describe('isDeploymentInputCorrect', () => {

    it('Correct input without specifying inAreas and exceptIn', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "location", undefined, undefined), true);
    });

    it('Correct inputs', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "location", ["milan", "france"], ["paris"]), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "city", ["milan", "france"], ["paris"]), true);
    });

    it('Input with wrong inEvery: area type does not exist', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "erfgfdsw"), false);
    });

    it('Input with wrong inAreas: not an array', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "location", "paris"), false);
    });

    it('Input with wrong inAreas: area is not specified in infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "location", ["paris", "erfgdg"]), false);
    });

    it('Input with wrong inAreas: the areas specified in inAreas does not have an area type bigger or equal than the area type specified in inEvery', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "continent", ["paris"]), false);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "country", ["paris"]), false);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "city", ["paris"]), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "location", ["paris"]), true);
    });

    it('Input with wrong exceptIn: not an array', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "location", undefined, "paris"), false);
    });

    it('Input with wrong exceptIn: area is not specified in infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "location", undefined, ["paris", "fjnrjefew"]), false);
    });

    it('Input with wrong exceptIn: the areas specified in exceptIn does not have an area type bigger or equal than the area type specified in inEvery', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "continent", undefined, ["paris"]), false);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "country", undefined, ["paris"]), false);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "city", undefined, ["paris"]), true);
      assert.equal(infrastructureParser.isDeploymentInputCorrect(infrastructureJson, "location", undefined, ["paris"]), true);
    });

  });

  describe('getAreaLevel', () => {

    it('Areas of standard infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "jhfieifjejf"), null);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "europe"), 0);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "france"), 1);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "turin"), 2);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "milan001"), 3);
    });

    it('Areas of one level infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/one-level-infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "jhfieifjejf"), null);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "milan001"), 0);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "milan002"), 0);
    });

    it('Areas of simple infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "jhfieifjejf"), null);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "europe"), 0);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "italy"), 1);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "milan"), 2);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "milan001"), 3);
      assert.equal(infrastructureParser.getAreaLevel(infrastructureJson, "milan002"), 3);
    });

  });

  describe('getAllLocations', () => {

    it('All locations of standard infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

      const locationObjects = infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, undefined);
      assert.equal(locationObjects.length, 8);
    });

    it('All locations of one level infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/one-level-infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

      const locationObjects = infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, undefined);
      assert.equal(locationObjects.length, 2);
      assert.isTrue(locationObjects[0].location_id === "milan001" || locationObjects[1].location_id === "milan001");
      assert.isTrue(locationObjects[0].location_id === "milan002" || locationObjects[1].location_id === "milan002");
    });

    it('All locations of simple infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

      const locationObjects = infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, undefined);
      assert.equal(locationObjects.length, 2);
      assert.isTrue(locationObjects[0].location_id === "milan001" || locationObjects[1].location_id === "milan001");
      assert.isTrue(locationObjects[0].location_id === "milan002" || locationObjects[1].location_id === "milan002");
    });

    it('Some locations of standard infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["italy"], undefined).length, 4);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["italy", "paris"], undefined).length, 6);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["paris001", "paris002"], undefined).length, 2);

      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, ["nice"]).length, 6);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, ["nice", "milan"]).length, 4);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, ["paris001", "paris002"]).length, 6);

      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["italy", "paris"], ["milan"]).length, 4);
    });

    it('Some locations of one level infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/one-level-infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["milan001"], undefined).length, 1);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["milan002"], undefined).length, 1);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["milan001", "milan002"], undefined).length, 2);

      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, ["milan001"]).length, 1);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, ["milan002"]).length, 1);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location",undefined, ["milan001", "milan002"]).length, 0);
    });

    it('Some locations of simple infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["europe"], undefined).length, 2);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["italy"], undefined).length, 2);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["milan"], undefined).length, 2);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["milan001", "milan002"], undefined).length, 2);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["milan001"], undefined).length, 1);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", ["milan002"], undefined).length, 1);

      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, ["europe"]).length, 0);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, ["italy"]).length, 0);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, ["milan"]).length, 0);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, ["milan001", "milan002"]).length, 0);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, ["milan001"]).length, 1);
      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, ["milan002"]).length, 1);
    });

    it('All locations of standard infrastructure with inEvery', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

      const locationObjectsContinent = infrastructureParser.getAllLocations(infrastructureJson, "continent", undefined, undefined);
      assert.equal(locationObjectsContinent.length, 1);
      assert.isTrue(locationObjectsContinent[0].location_id === "europe" && locationObjectsContinent[0].openfaas_gateway === "http://10.211.55.10:31112");

      const locationObjectsCountry = infrastructureParser.getAllLocations(infrastructureJson, "country", undefined, undefined);
      assert.equal(locationObjectsCountry.length, 2);
      assert.isTrue(locationObjectsCountry[0].location_id === "italy" || locationObjectsCountry[1].location_id === "italy");
      assert.isTrue(locationObjectsCountry[0].location_id === "france" || locationObjectsCountry[1].location_id === "france");

      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "city", undefined, undefined).length, 4);

      assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, undefined).length, 8);
    });

    it('Some locations of standard infrastructure with inEvery', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

      const locationObjects1 = infrastructureParser.getAllLocations(infrastructureJson, "continent", ["europe"], undefined);
      assert.equal(locationObjects1.length, 1);
      assert.isTrue(locationObjects1[0].location_id === "europe" && locationObjects1[0].openfaas_gateway === "http://10.211.55.10:31112");

      const locationObjects2 = infrastructureParser.getAllLocations(infrastructureJson, "country", ["italy"], undefined);
      assert.equal(locationObjects2.length, 1);
      assert.isTrue(locationObjects2[0].location_id === "italy" && locationObjects2[0].openfaas_gateway === "http://10.211.55.11:31112");

      const locationObjects3 = infrastructureParser.getAllLocations(infrastructureJson, "country", ["europe"], ["france"]);
      assert.equal(locationObjects3.length, 1);
      assert.isTrue(locationObjects3[0].location_id === "italy" && locationObjects3[0].openfaas_gateway === "http://10.211.55.11:31112");

      const locationObjects4 = infrastructureParser.getAllLocations(infrastructureJson, "city", ["italy"], ["milan"]);
      assert.equal(locationObjects4.length, 1);
      assert.isTrue(locationObjects4[0].location_id === "turin" && locationObjects4[0].openfaas_gateway === "http://10.211.55.15:31112");

      const locationObjects5 = infrastructureParser.getAllLocations(infrastructureJson, "city", ["europe"], ["nice", "paris"]);
      assert.equal(locationObjects5.length, 2);
      assert.isTrue(locationObjects5[0].location_id === "milan" || locationObjects5[1].location_id === "milan");
      assert.isTrue(locationObjects5[0].location_id === "turin" || locationObjects5[1].location_id === "turin");

      const locationObjects6 = infrastructureParser.getAllLocations(infrastructureJson, "city", ["france"], ["paris"]);
      assert.equal(locationObjects6.length, 1);
      assert.isTrue(locationObjects6[0].location_id === "nice" && locationObjects6[0].openfaas_gateway === "http://10.211.55.22:31112");
    });
  });
});
