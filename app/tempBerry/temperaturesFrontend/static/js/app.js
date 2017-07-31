"use strict";

// define modules
angular.module('screens', []);
angular.module('services', []);
angular.module('widgets', []);

// define app module
var app = angular.module('app', [
    'ngResource',
    'ui.router',
    'nvd3',
    'screens',
    'services',
    'widgets'
]);

app.config(function($resourceProvider, $urlRouterProvider, $stateProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;

  $urlRouterProvider.otherwise('/');


  $stateProvider.state(
      'main', {
          url: '/',
          component: 'temperaturesDashboard'
      }
  ).state(
      'detail', {
          url: '/details/{sensorId}',
          component: 'temperaturesDetail',
          resolve: {
              'sensorId': function($stateParams) {
                  return $stateParams.sensorId;
              }
          }
      }
  );
});
