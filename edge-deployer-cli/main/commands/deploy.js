'use strict';

const chalk = require('chalk');
const shell = require("shelljs");
const fs = require('fs');
const infrastructureParser = require('./../utils/infrastructureParser');

module.exports = function deploy(functionName, infrastructure, {inEvery, inAreas, exceptIn, yaml}) {
    try {
        // Read json file.
        const infrastructureString = fs.readFileSync(infrastructure, 'utf8');
        const infrastructureJson = JSON.parse(infrastructureString);

        // Check correctness of infrastructure file.
        console.log(chalk.white.bold("🔄 Checking if infrastructure is correct."));
        if(!infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson)) {
            console.log(chalk.red.bold("❌ The infrastructure JSON is NOT correct."));
            return;
        }
        console.log(chalk.green.bold("✅ The infrastructure JSON is correct."));

        // Check correctness of input.
        console.log(chalk.white.bold("🔄 Checking if input is correct."));
        if(!infrastructureParser.isDeploymentInputCorrect(infrastructureJson, inEvery, inAreas, exceptIn)) {
            console.log(chalk.red.bold("❌ The input is NOT correct."));
            return;
        }
        console.log(chalk.green.bold("✅ The input is correct."));

        // Get locations to deploy.
        console.log(chalk.white.bold("🔄 Getting all locations of infrastructure."));
        const listOfLocations = infrastructureParser.getAllLocations(infrastructureJson, inEvery, inAreas, exceptIn);
        if(listOfLocations.length === 0) {
            console.log(chalk.red.bold("❌ The input does not correspond to any location."));
            return;
        }

        // Deploy to all locations.
        for(const location of listOfLocations) {
            const envVariablesString = "--env=LOCATION_ID=" + location.location_id + " --env=EDGE_INFRASTRUCTURE='" + infrastructureString + "' --env=REDIS_HOST=" + location.redis_host + " --env=REDIS_PORT=" + location.redis_port + " --env=REDIS_PASSWORD=" + location.redis_password;
            console.log(chalk.white.bold("📶 Deploying on location: \"" + location.location_id + "\", gateway: \"" + location.openfaas_gateway + "\"."));
            shell.exec("echo " + location.openfaas_password + " | faas-cli login --username admin --password-stdin --gateway " + location.openfaas_gateway);
            shell.exec("faas-cli deploy --filter " + functionName + " --yaml " + yaml + " --gateway " + location.openfaas_gateway + " " + envVariablesString);
        }
    } catch(err) {
        console.error(err);
    }
}
