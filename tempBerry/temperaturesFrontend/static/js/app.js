var app = angular.module('app', ['ngResource']);

app.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});

app.controller('MainCtrl', function($scope, $resource, $timeout) {
    var api = $resource('/api/temperatures/latest/');

    $scope.response = [];

    $scope.getdata = function() {
        api.query().$promise.then(function (response) {
            $scope.response = response;
        });

        $timeout($scope.getdata, 5000);
    };

    $scope.getdata();
});