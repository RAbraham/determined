#!/usr/bin/env node
/* eslint-disable no-console */

const express = require('express');
const morgan = require('morgan');
const request = require('request');

if (process.argv.length < 3) {
  console.error('./proxy.js <target> <port>');
  process.exit(1);
}

const PORT = process.argv[3] || 8100;
const fixedProxyTarget = process.argv[2];

const app = express();
app.use(morgan('dev'));

const proxyTo = (targetServer) => {
  return (req, res) => {
    const url = targetServer + req.url;
    res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
    res.setHeader('Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    res.setHeader('Access-Control-Allow-Methods', 'GET,HEAD,OPTIONS,POST,PUT');
    res.setHeader(
      'Access-Control-Allow-Headers',
      'authorization, Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type,'
      + ' Access-Control-Request-Method, Access-Control-Request-Headers',
    );

    if ('OPTIONS' === req.method) {
      res.send(200);
    } else {
      req.pipe(request({ qs:req.query, uri: url })).pipe(res);
    }
  };
};

app.use('/dynamic/:protocol/:target', function(req, res) {
  const targetServer = req.params.protocol + '://' + req.params.target;
  return proxyTo(targetServer)(req, res);
});

app.use('/fixed', proxyTo(fixedProxyTarget));

app.listen(PORT);
console.log(`Listening on http://localhost:${PORT}`);
console.log(`Proxying requests to http://localhost:${PORT}/fixed to ${fixedProxyTarget}`);
