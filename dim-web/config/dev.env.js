'use strict';
const merge = require('webpack-merge');
const prodEnv = require('./prod.env');

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  DIM_LOGIN: '"https://test.example.com:5000/login"',
  DIM_RPC: '"https://test.example.com:5000/jsonrpc"',
  LOGIN: '"https://test.example.com"',
  LOGOUT: '"https://test.example.com/logout"',
  BASE_URL: '"/"',
  SLEEP: 1000
});
