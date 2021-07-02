#! /usr/bin/env node
'use strict';

const { program } = require('commander');
const deploy = require('./main/commands/deploy');

program
    .command('deploy <infrastructure>')
    .description('Deploy test')
    .action(deploy);

program.parse();