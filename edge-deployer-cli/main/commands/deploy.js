'use strict';

const chalk = require('chalk');
const shell = require("shelljs");
const fs = require('fs');
const infrastructureParser = require('./../utils/infrastructureParser')

module.exports = function deploy(infrastructure, {yaml}) {
    try {
        // Read json file.
        const data = fs.readFileSync(infrastructure, 'utf8');
        const infrastructureJson = JSON.parse(data);

        // Check correctness of file.
        console.log(chalk.white.bold("🔄 Checking if infrastructure is correct."));
        if(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson)) {
            console.log(chalk.green.bold("✅ The infrastructure JSON is correct."));
            console.log(chalk.white.bold("🔄 Getting all locations of infrastructure."));
            const listOfLocations = infrastructureParser.getAllLocations(infrastructureJson);
            for(const location of listOfLocations) {
                const gateway = "http://" + location.ip + ":" + location.port;
                console.log(chalk.white.bold("📶 Deploying on " + gateway + "."));
                shell.exec("echo " + location.password + " | faas-cli login --username admin --password-stdin --gateway " + gateway);
                shell.exec("faas-cli deploy --yaml " + yaml + " --gateway " + gateway);
            }
        } else {
            console.log(chalk.red.bold("❌ The infrastructure JSON is NOT correct."));
        }
    } catch(err) {
        console.error(err);
    }
}
