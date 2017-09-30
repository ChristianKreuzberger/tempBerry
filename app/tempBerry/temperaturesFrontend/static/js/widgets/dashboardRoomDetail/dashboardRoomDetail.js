(function() {
    'use strict';

    var
        module = angular.module('widgets');

    module.directive('dashboardRoomDetailWidget', function() {
        return {
            restrict: 'E',
            templateUrl: 'js/widgets/dashboardRoomDetail/dashboardRoomDetail.html',
            scope: {
                "room": "="
            }
        };
    });

})();