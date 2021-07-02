/* eslint-disable promise/no-nesting */
'use strict';

// Dependencies
const chai = require('chai');
const assert = chai.assert;
const sinon = require('sinon');
const fs = require('fs');

describe('Tests', () => {

    before(() => {

    });

    afterEach(() => {

    });

    after(() => {

    });

    describe('infrastructureParser', () => {

        let infrastructureParser;
        before(() => {
            infrastructureParser = require('../main/utils/infrastructureParser');
        });

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

});
