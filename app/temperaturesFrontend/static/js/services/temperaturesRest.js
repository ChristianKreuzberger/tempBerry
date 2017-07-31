(function() {
    'use strict';

    var
        module = angular.module('services');

    module.service('temperaturesRestService', function($resource) {
        return $resource('/api/temperatures/',
            {
            },
            {
                'getLatest': {
                    'url': '/api/temperatures/latest/',
                    'method': 'GET',
                    'isArray': true
                }
            }
        );
    });
})();
