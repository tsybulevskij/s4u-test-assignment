(function(){
    'use strict';

    angular
        .module('eglobal')
        .factory('AccountService', AccountService);

    AccountService.$inject = ['$http', 'API'];

    function AccountService($http, API) {

        var service = {
            allAccounts: AllAccounts,
            createAccount: createAccount,
            AccountTransactions: AccountTransactions,
            CreateTransactions: CreateTransactions
        };

        return service;

        function AllAccounts(){
            return $http({
                method: 'GET',
                url: API.domain + '/accounts/'
            })
        }

        function createAccount(data) {
            return $http({
                method: 'POST',
                url: API.domain + '/accounts/',
                data: data
            })
        }

        function AccountTransactions(id){
            return $http({
                method: 'GET',
                url: API.domain + '/accounts/' + id + '/transactions/'
            })
        }

        function CreateTransactions(data){
            return $http({
                method: 'POST',
                url: API.domain + '/transactions/',
                  data: data
            })
        }
    }
})();
