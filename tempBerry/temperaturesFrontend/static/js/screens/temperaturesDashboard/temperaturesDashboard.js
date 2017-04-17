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


        vm.deviceIdToRoomName = function(deviceId) {

            if (deviceId == 20) {
                return "Arbeitszimmer";
            } else if (deviceId == 37) {
                return "Außensensor";
            } else if (deviceId == 53) {
                return "Schlafzimmer";
            } else if (deviceId == 92) {
                return "Badezimmer";
            } else if (deviceId == 215) {
                return "Gästezimmer";
            }
            return "Unbekannt";
        };



        var init = function() {

        };

        init();

        $scope.$on('$destroy', function() {
            $timeout.cancel(timer);
        });

        vm.response = [];

        vm.getdata = function() {
            temperaturesRestService.getLatest().$promise.then(function (response) {
                vm.response = response;
            });

            timer = $timeout(vm.getdata, 5000);
        };

        vm.getdata();
    });
})();
