(function() {
    'use strict';

    var
        module = angular.module('screens');

    module.component('temperaturesDashboard', {
        templateUrl: 'js/screens/temperaturesDashboard/temperaturesDashboard.html',
        controller: 'TemperaturesDashboardController',
        controllerAs: 'vm',
        bindings: {
        }
    });

    module.controller('TemperaturesDashboardController', function($scope, $timeout, temperaturesRestService) {

        var
            vm = this,
            timer = undefined;

        var init = function() {

        };

        init();

        $scope.$on('$destroy', function() {
            $timeout.cancel(timer);
        });

        vm.entries = [];

        vm.getdata = function() {
            temperaturesRestService.getLatest().$promise.then(function (response) {
                vm.entries = response;
            });

            timer = $timeout(vm.getdata, 5000);
        };

        vm.getdata();
    });
})();
