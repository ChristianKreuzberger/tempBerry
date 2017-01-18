var screens = angular.module('screens', []);
var services = angular.module('services', []);
var app = angular.module('app', [
    'ngResource',
    'ui.router',
    'nvd3',
    'screens',
    'services'
]);


app.config(function($resourceProvider, $stateProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;

  $stateProvider.state(
      'main', {
          url: '',
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
