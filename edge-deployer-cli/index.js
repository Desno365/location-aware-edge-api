#! /usr/bin/env node
'use strict';

const { program } = require('commander');
const deploy = require('./main/commands/deploy');

program
    .command('deploy <infrastructure>')
    .description('Deploys functions to the infrastructure specified.')
    .option('-f, --yaml <string>', 'Path to the YAML file describing function(s).', 'stack.yml')
    .action(deploy);

program.parse();