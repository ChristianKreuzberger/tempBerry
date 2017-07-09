(function() {
    'use strict';

    var
        module = angular.module('widgets');

    module.directive('roomDetail', function() {
        return {
            controller: 'RoomDetailController',
            restrict: 'E',
            templateUrl: 'js/widgets/roomDetail/roomDetail.html',
            scope: {
                'entry': '='
            }
        };
    });

    module.controller('RoomDetailController', ["$scope", function($scope) {
        console.log("Room Detail Controller initialized");

        $scope.deviceIdToRoomName = function(deviceId) {

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
    }]);
})();