#! /usr/bin/env node
'use strict';

const { program } = require('commander');
const checkInfrastructure = require('./main/commands/checkInfrastructure');
const deploy = require('./main/commands/deploy');

program
    .command('check-infrastructure <infrastructure>')
    .description('Check if the infrastructure JSON is correct.')
    .action(checkInfrastructure);

// Note: <areas...> signifies that it can be more than one area, but because we are using <> that means it should include at least one.
// Note: When an argument is required, we use <ARG_NAME>, whereas if it’s optional, we use [ARG_NAME].
program
    .command('deploy <functionName> <infrastructure>')
    .description('Deploys the function to the infrastructure specified.')
    .option('--inEvery <areaTypeIdentifier>', 'In which area type to deploy the function. If not specified the function is deployed to the lowest level.')
    .option('--inAreas <areas...>', 'The name of the areas in which to deploy the function. If not specified the function is deployed everywhere.')
    .option('--exceptIn <areas...>', 'The name of the areas in which to NOT deploy the function.')
    .option('-f, --yaml <path>', 'Path to the YAML file describing the function.', 'stack.yml')
    .action(deploy);

program.parse();