(function() {
    angular
        .module('eglobal')
        .constant('API', {domain: 'http://127.0.0.1:8000'})
        .config(routing)
        .config(config)
        .run(run);


    config.$inject = ['$httpProvider'];
    function config($httpProvider) {
        // for cross domain requests
        $httpProvider.defaults.withCredentials = true;

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }


    run.$inject = ['$rootScope', '$state', '$http', '$cookies'];
    function run($rootScope, $state, $http, $cookies){
        $http.defaults.headers.common['X-CSRFToken'] = $cookies.get('csrftoken');
        $http.defaults.headers.common['Api-Key'] = '051c00dbdb8686e95e56c8d18e3fb37f274f41c5';
    }


    routing.$inject = ['$stateProvider', '$urlRouterProvider', '$locationProvider'];
    function routing($stateProvider, $urlRouterProvider, $locationProvider) {
        $locationProvider.hashPrefix('');
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('index', {
                url: '/',
                templateUrl: '/static/app/views/account.html',
                controller: 'AccountCtrl'
            })
    }

})();