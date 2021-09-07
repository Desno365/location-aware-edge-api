/* eslint-disable promise/no-nesting */
'use strict';

// Dependencies
const chai = require('chai');
const assert = chai.assert;
const fs = require('fs');
const edgeDb = require('../functions-main/common/edge-db/edge-db');
const savingTypeEnum = require('../functions-main/common/edge-db/savingTypeEnum');

describe('edgeDb', () => {

  describe('withDataDomain', () => {

    it('Local write in location', () => {
      // Prepare environment.
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      process.env.EDGE_INFRASTRUCTURE = fs.readFileSync(infrastructurePath, 'utf8');
      process.env.LOCATION_ID = "paris002";
      process.env.EDGE_DEPLOYMENT_IN_EVERY = "location";
      const edgeDbClientWithDataDomain = edgeDb.withDataDomain({ referringAreaType: "location", ttl: 2000 });

      assert.equal(edgeDbClientWithDataDomain.ownAreaTypeLevel, 3);
      assert.equal(edgeDbClientWithDataDomain.referringAreaTypeLevel, 3);
      assert.equal(edgeDbClientWithDataDomain.savingType, savingTypeEnum.ONLY_LOCAL);
    });

    it('Local write in country', () => {
      // Prepare environment.
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      process.env.EDGE_INFRASTRUCTURE = fs.readFileSync(infrastructurePath, 'utf8');
      process.env.LOCATION_ID = "italy";
      process.env.EDGE_DEPLOYMENT_IN_EVERY = "country";
      const edgeDbClientWithDataDomain = edgeDb.withDataDomain({ referringAreaType: "country", ttl: 2000 });

      assert.equal(edgeDbClientWithDataDomain.ownAreaTypeLevel, 1);
      assert.equal(edgeDbClientWithDataDomain.referringAreaTypeLevel, 1);
      assert.equal(edgeDbClientWithDataDomain.savingType, savingTypeEnum.ONLY_LOCAL);
    });

    it('Single remote write in country from location', () => {
      // Prepare environment.
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      process.env.EDGE_INFRASTRUCTURE = fs.readFileSync(infrastructurePath, 'utf8');
      process.env.LOCATION_ID = "paris002";
      process.env.EDGE_DEPLOYMENT_IN_EVERY = "location";
      const edgeDbClientWithDataDomain = edgeDb.withDataDomain({ referringAreaType: "country", ttl: 2000, saveAlsoInIntermediateLevels: false });

      assert.equal(edgeDbClientWithDataDomain.ownAreaTypeLevel, 3);
      assert.equal(edgeDbClientWithDataDomain.referringAreaTypeLevel, 1);
      assert.equal(edgeDbClientWithDataDomain.savingType, savingTypeEnum.SINGLE_REMOTE);
      assert.equal(edgeDbClientWithDataDomain.savingLocationsList.length, 1);
      assert.equal(edgeDbClientWithDataDomain.savingLocationsList[0].location_id, "france");
      assert.equal(edgeDbClientWithDataDomain.savingLocationsList[0].openfaas_gateway, "http://10.211.55.18:31112");
    });

    it('Single remote write in continent from country', () => {
      // Prepare environment.
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      process.env.EDGE_INFRASTRUCTURE = fs.readFileSync(infrastructurePath, 'utf8');
      process.env.LOCATION_ID = "france";
      process.env.EDGE_DEPLOYMENT_IN_EVERY = "country";
      const edgeDbClientWithDataDomain = edgeDb.withDataDomain({ referringAreaType: "continent", ttl: 2000, saveAlsoInIntermediateLevels: false });

      assert.equal(edgeDbClientWithDataDomain.ownAreaTypeLevel, 1);
      assert.equal(edgeDbClientWithDataDomain.referringAreaTypeLevel, 0);
      assert.equal(edgeDbClientWithDataDomain.savingType, savingTypeEnum.SINGLE_REMOTE);
      assert.equal(edgeDbClientWithDataDomain.savingLocationsList.length, 1);
      assert.equal(edgeDbClientWithDataDomain.savingLocationsList[0].location_id, "europe");
      assert.equal(edgeDbClientWithDataDomain.savingLocationsList[0].openfaas_gateway, "http://10.211.55.10:31112");
    });

    it('Write with intermediate in country from location', () => {
      // Prepare environment.
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      process.env.EDGE_INFRASTRUCTURE = fs.readFileSync(infrastructurePath, 'utf8');
      process.env.LOCATION_ID = "paris002";
      process.env.EDGE_DEPLOYMENT_IN_EVERY = "location";
      const edgeDbClientWithDataDomain = edgeDb.withDataDomain({ referringAreaType: "country", ttl: 2000, saveAlsoInIntermediateLevels: true });

      assert.equal(edgeDbClientWithDataDomain.ownAreaTypeLevel, 3);
      assert.equal(edgeDbClientWithDataDomain.referringAreaTypeLevel, 1);
      assert.equal(edgeDbClientWithDataDomain.savingType, savingTypeEnum.SAVE_ALSO_IN_INTERMEDIATE_LEVELS);
      assert.equal(edgeDbClientWithDataDomain.savingLocationsList.length, 2);
      assert.isTrue((edgeDbClientWithDataDomain.savingLocationsList[0].location_id === "france" && edgeDbClientWithDataDomain.savingLocationsList[0].openfaas_gateway === "http://10.211.55.18:31112" )
        || (edgeDbClientWithDataDomain.savingLocationsList[1].location_id === "france" && edgeDbClientWithDataDomain.savingLocationsList[1].openfaas_gateway === "http://10.211.55.18:31112"));
      assert.isTrue((edgeDbClientWithDataDomain.savingLocationsList[0].location_id === "paris" && edgeDbClientWithDataDomain.savingLocationsList[0].openfaas_gateway === "http://10.211.55.19:31112" )
        || (edgeDbClientWithDataDomain.savingLocationsList[1].location_id === "paris" && edgeDbClientWithDataDomain.savingLocationsList[1].openfaas_gateway === "http://10.211.55.19:31112"));
    });

    it('Write with intermediate in continent from city', () => {
      // Prepare environment.
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      process.env.EDGE_INFRASTRUCTURE = fs.readFileSync(infrastructurePath, 'utf8');
      process.env.LOCATION_ID = "paris";
      process.env.EDGE_DEPLOYMENT_IN_EVERY = "city";
      const edgeDbClientWithDataDomain = edgeDb.withDataDomain({ referringAreaType: "continent", ttl: 2000, saveAlsoInIntermediateLevels: true });

      assert.equal(edgeDbClientWithDataDomain.ownAreaTypeLevel, 2);
      assert.equal(edgeDbClientWithDataDomain.referringAreaTypeLevel, 0);
      assert.equal(edgeDbClientWithDataDomain.savingType, savingTypeEnum.SAVE_ALSO_IN_INTERMEDIATE_LEVELS);
      assert.equal(edgeDbClientWithDataDomain.savingLocationsList.length, 2);
      assert.isTrue((edgeDbClientWithDataDomain.savingLocationsList[0].location_id === "europe" && edgeDbClientWithDataDomain.savingLocationsList[0].openfaas_gateway === "http://10.211.55.10:31112" )
        || (edgeDbClientWithDataDomain.savingLocationsList[1].location_id === "europe" && edgeDbClientWithDataDomain.savingLocationsList[1].openfaas_gateway === "http://10.211.55.10:31112"));
      assert.isTrue((edgeDbClientWithDataDomain.savingLocationsList[0].location_id === "france" && edgeDbClientWithDataDomain.savingLocationsList[0].openfaas_gateway === "http://10.211.55.18:31112" )
        || (edgeDbClientWithDataDomain.savingLocationsList[1].location_id === "france" && edgeDbClientWithDataDomain.savingLocationsList[1].openfaas_gateway === "http://10.211.55.18:31112"));
    });

  });

});
