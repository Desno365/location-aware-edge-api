'use strict';

const chalk = require('chalk');
const fs = require('fs');
const infrastructureParser = require('./../utils/infrastructureParser');

module.exports = function checkInfrastructure(infrastructure) {
    try {
        // Read json file.
        const data = fs.readFileSync(infrastructure, 'utf8');
        const infrastructureJson = JSON.parse(data);

        // Check correctness of infrastructure file.
        console.log(chalk.white.bold("🔄 Checking if infrastructure is correct."));
        if(!infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson)) {
            console.log(chalk.red.bold("❌ The infrastructure JSON is NOT correct."));
            return;
        }
        console.log(chalk.green.bold("✅ The infrastructure JSON is correct."));
    } catch(err) {
        console.error(err);
    }
}