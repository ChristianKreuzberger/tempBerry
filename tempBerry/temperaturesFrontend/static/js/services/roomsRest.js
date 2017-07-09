(function() {
    'use strict';

    var
        module = angular.module('services');

    module.service('roomsRestService', function($resource) {
        return $resource('/api/rooms/:id',
            {
                'id': '@id'
            },
            {
                'getAggregates24h': {
                    'url': '/api/rooms/:id/aggregates_24h/',
                    'method': 'GET',
                    'isArray': false
                }
            }
        );
    });
})();
