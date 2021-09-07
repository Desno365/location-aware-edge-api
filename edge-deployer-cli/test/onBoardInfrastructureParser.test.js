/* eslint-disable promise/no-nesting */
'use strict';

// Dependencies
const chai = require('chai');
const assert = chai.assert;
const fs = require('fs');
const infrastructureParser = require('../main/utils/infrastructureParser');
const onBoardInfrastructureParser = require('../../functions-edge/common/edge-db/onBoardInfrastructureParser');

describe('onBoardInfrastructureParser', () => {

  describe('getLocationObjectOfReferringAreaInInfrastructure', () => {

    it('Referring area of standard infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice002", 0).location_id, "europe");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice002", 0).openfaas_gateway, "http://10.211.55.10:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice002", 1).location_id, "france");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice002", 1).openfaas_gateway, "http://10.211.55.18:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice002", 2).location_id, "nice");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice002", 2).openfaas_gateway, "http://10.211.55.22:31112");

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice001", 0).location_id, "europe");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice001", 0).openfaas_gateway, "http://10.211.55.10:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice001", 1).location_id, "france");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice001", 1).openfaas_gateway, "http://10.211.55.18:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice001", 2).location_id, "nice");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice001", 2).openfaas_gateway, "http://10.211.55.22:31112");

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 0).location_id, "europe");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 0).openfaas_gateway, "http://10.211.55.10:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 1).location_id, "italy");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 1).openfaas_gateway, "http://10.211.55.11:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 2).location_id, "milan");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 2).openfaas_gateway, "http://10.211.55.12:31112");

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice", 0).location_id, "europe");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice", 0).openfaas_gateway, "http://10.211.55.10:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice", 1).location_id, "france");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice", 1).openfaas_gateway, "http://10.211.55.18:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice", 2).location_id, "nice");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "nice", 2).openfaas_gateway, "http://10.211.55.22:31112");

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "france", 0).location_id, "europe");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "france", 0).openfaas_gateway, "http://10.211.55.10:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "france", 1).location_id, "france");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "france", 1).openfaas_gateway, "http://10.211.55.18:31112");

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "europe", 0).location_id, "europe");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "europe", 0).openfaas_gateway, "http://10.211.55.10:31112");
    });

    it('Referring area of one level infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/one-level-infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 0).location_id, "milan001");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 0).openfaas_gateway, "http://10.211.55.22:31112");

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 0).location_id, "milan002");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 0).openfaas_gateway, "http://10.211.55.23:31112");
    });

    it('Referring area of simple infrastructure', () => {
      const infrastructurePath = "./test/test-infrastructures/simple-infrastructure-correct.json";
      const data = fs.readFileSync(infrastructurePath, 'utf8');
      const infrastructureJson = JSON.parse(data);
      assert.equal(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson), true);

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 0).location_id, "europe");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 0).openfaas_gateway, "http://10.211.55.20:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 1).location_id, "italy");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 1).openfaas_gateway, "http://10.211.55.21:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 2).location_id, "milan");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan001", 2).openfaas_gateway, "http://10.211.55.22:31112");

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 0).location_id, "europe");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 0).openfaas_gateway, "http://10.211.55.20:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 1).location_id, "italy");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 1).openfaas_gateway, "http://10.211.55.21:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 2).location_id, "milan");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan002", 2).openfaas_gateway, "http://10.211.55.22:31112");

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan", 0).location_id, "europe");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan", 0).openfaas_gateway, "http://10.211.55.20:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan", 1).location_id, "italy");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan", 1).openfaas_gateway, "http://10.211.55.21:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan", 2).location_id, "milan");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "milan", 2).openfaas_gateway, "http://10.211.55.22:31112");

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "italy", 0).location_id, "europe");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "italy", 0).openfaas_gateway, "http://10.211.55.20:31112");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "italy", 1).location_id, "italy");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "italy", 1).openfaas_gateway, "http://10.211.55.21:31112");

      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "europe", 0).location_id, "europe");
      assert.equal(onBoardInfrastructureParser.getLocationObjectOfReferringAreaInInfrastructure(infrastructureJson, "europe", 0).openfaas_gateway, "http://10.211.55.20:31112");
    });

  });

});
