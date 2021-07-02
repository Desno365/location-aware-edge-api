'use strict';

const chalk = require('chalk');
const shell = require("shelljs");
const fs = require('fs');
const infrastructureParser = require('./../utils/infrastructureParser')

module.exports = function deploy(infrastructure) {
    try {
        // Read json file.
        const data = fs.readFileSync(infrastructure, 'utf8');
        const infrastructureJson = JSON.parse(data);

        // Check correctness of file.
        if(infrastructureParser.isInfrastructureJsonCorrect(infrastructureJson)) {
            console.log(chalk.green.bold("✅ The infrastructure JSON is correct."));
        } else {
            console.log(chalk.red.bold("❌ The infrastructure JSON is NOT correct."));
        }
    } catch(err) {
        console.error(err);
    }
    //shell.exec("echo 936af6e5370686ce2ddad6ab03891e471ccd5969 | faas-cli login --username admin --password-stdin --gateway http://10.211.55.22:31112");
    //shell.exec("faas-cli deploy --yaml stack.yml --gateway http://10.211.55.22:31112");
}
