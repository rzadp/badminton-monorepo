
/* eslint-disable import/first, no-undef, no-unused-vars */
import 'regenerator-runtime/runtime';
require('babel-core/register');
require('babel-polyfill');
import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/app';
import Builder from './builder';
require('./styles/app.scss');

(async() => {
  const services = await Builder.build();
  ReactDOM.render(<App services={services}/>, document.getElementById('app'));
})();

/* eslint-enable import/first no-undef */
