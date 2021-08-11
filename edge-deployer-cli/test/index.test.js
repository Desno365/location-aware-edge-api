/* eslint-disable promise/no-nesting */
'use strict';

// Dependencies
const chai = require('chai');
const assert = chai.assert;
const sinon = require('sinon');
const fs = require('fs');
const infrastructureParser = require('../main/utils/infrastructureParser');
const onBoardInfrastructureParser = require('../../functions-edge/common/edge-db/onBoardInfrastructureParser');

describe('Tests', () => {

    before(() => {

    });

    afterEach(() => {

    });

    after(() => {

    });

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
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, undefined).length, 8);
            });

            it('All locations of one level infrastructure', () => {
                const infrastructurePath = "./test/test-infrastructures/one-level-infrastructure-correct.json";
                const data = fs.readFileSync(infrastructurePath, 'utf8');
                const infrastructureJson = JSON.parse(data);
                assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, undefined).length, 2);
            });

            it('All locations of simple infrastructure', () => {
                const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-correct.json";
                const data = fs.readFileSync(infrastructurePath, 'utf8');
                const infrastructureJson = JSON.parse(data);
                assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, undefined).length, 2);
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
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "continent", undefined, undefined).length, 1);
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "country", undefined, undefined).length, 2);
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "city", undefined, undefined).length, 4);
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "location", undefined, undefined).length, 8);
            });

            it('Some locations of standard infrastructure with inEvery', () => {
                const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
                const data = fs.readFileSync(infrastructurePath, 'utf8');
                const infrastructureJson = JSON.parse(data);
                assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "continent", ["europe"], undefined).length, 1);
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "country", ["italy"], undefined).length, 1);
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "country", ["europe"], ["france"]).length, 1);
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "city", ["italy"], ["milan"]).length, 1);
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "city", ["europe"], ["nice", "paris"]).length, 2);
                assert.equal(infrastructureParser.getAllLocations(infrastructureJson, "city", ["france"], ["paris"]).length, 1);
            });
        });
    });

    describe('onBoardInfrastructureParser', () => {

        describe('getLocationIdOfReferringAreaInInfrastructure', () => {

            it('Referring area of standard infrastructure', () => {
                const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
                const data = fs.readFileSync(infrastructurePath, 'utf8');
                const infrastructureJson = JSON.parse(data);
                assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "nice002", 0), "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "nice002", 1), "paris001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "nice002", 2), "nice001");

                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "nice001", 0), "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "nice001", 1), "paris001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "nice001", 2), "nice001");

                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "paris002", 0), "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "paris002", 1), "paris001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "paris002", 2), "paris001");

                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 0), "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 1), "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 2), "milan001");
            });

            it('Referring area of one level infrastructure', () => {
                const infrastructurePath = "./test/test-infrastructures/one-level-infrastructure-correct.json";
                const data = fs.readFileSync(infrastructurePath, 'utf8');
                const infrastructureJson = JSON.parse(data);
                assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 0), "milan001");

                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 0), "milan001");
            });

            it('Referring area of simple infrastructure', () => {
                const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-correct.json";
                const data = fs.readFileSync(infrastructurePath, 'utf8');
                const infrastructureJson = JSON.parse(data);
                assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 0), "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 1), "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 2), "milan001");

                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 0), "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 1), "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationIdOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 2), "milan001");
            });

        });

        describe('getLocationObject', () => {

            it('getLocationObject of standard infrastructure', () => {
                const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
                const data = fs.readFileSync(infrastructurePath, 'utf8');
                const infrastructureJson = JSON.parse(data);
                assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "nice002").location_id, "nice002");
                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "nice002").openfaas_gateway, "http://10.211.55.29:31112");

                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "milan001").location_id, "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "milan001").openfaas_gateway, "http://10.211.55.22:31112");

                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "turin002").location_id, "turin002");
                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "turin002").openfaas_gateway, "http://10.211.55.25:31112");
            });

            it('getLocationObject of one level infrastructure', () => {
                const infrastructurePath = "./test/test-infrastructures/one-level-infrastructure-correct.json";
                const data = fs.readFileSync(infrastructurePath, 'utf8');
                const infrastructureJson = JSON.parse(data);
                assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "milan001").location_id, "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "milan001").openfaas_gateway, "http://10.211.55.22:31112");

                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "milan002").location_id, "milan002");
                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "milan002").openfaas_gateway, "http://10.211.55.23:31112");
            });

            it('getLocationObject of simple infrastructure', () => {
                const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-correct.json";
                const data = fs.readFileSync(infrastructurePath, 'utf8');
                const infrastructureJson = JSON.parse(data);
                assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "milan001").location_id, "milan001");
                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "milan001").openfaas_gateway, "http://10.211.55.22:31112");

                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "milan002").location_id, "milan002");
                assert.equal(onBoardInfrastructureParser.getLocationObject(infrastructureJson, "milan002").openfaas_gateway, "http://10.211.55.23:31112");
            });

        });

    });

});
