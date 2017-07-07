(function() {
    'use strict';

    angular
        .module('eglobal')
        .controller('AccountCtrl', AccountCtrl);

    AccountCtrl.$inject = ['$scope', '$state', 'AccountService'];
    // Controller that respond for displaying Menu.
    function AccountCtrl($scope, $state, AccountService) {
        $scope.getAllAccounts = getAllAccounts;
        $scope.CreateAccount = CreateAccount;
        $scope.AccountTransactions = AccountTransactions;
        $scope.CreateTransactions = CreateTransactions;

        $scope.newAccount = {};
        $scope.newTransaction = {};
        $scope.errors = {
            global: [],
            createAccount: [],
            createTransaction: []
        };

        activate();

        function activate() {
            getAllAccounts();
        }

        function GettAPIErrorMessage(response) {
            var status = response.status;

            if (status == 400) {
                for (var field_name in response.data.message){
                    var message =  field_name == 'non_field_error' ? '' : field_name + ': ' ;
                    response.data.message[field_name].forEach(function (error){
                        message += error;
                    })
                    return message

                }
                return response.data.message;
            }
            if(status >= 500 && status < 600 && !response.data.message){
                return status + ': Internal server error';
            }
            else{
                return response.data.message;
            }
        }

        function getAllAccounts() {
            AccountService.allAccounts().then(
            function (response){
                $scope.accounts = response.data;
            },
            function (response) {
                $scope.errors.global = GettAPIErrorMessage(response);
            })
        }

        function CreateAccount() {
            AccountService.createAccount($scope.newAccount).then(
            function (response){
                getAllAccounts();
            },
            function (response) {
                $scope.errors.createAccount = GettAPIErrorMessage(response);
            })
        }

        function AccountTransactions(acc) {
            $scope.selectedAccount = acc;
            AccountService.AccountTransactions(acc.id).then(
            function (response){
                $scope.transactions = response.data
            },
            function (response) {
                $scope.errors.global = GettAPIErrorMessage(response)
            })
        }

        function CreateTransactions() {
            AccountService.CreateTransactions($scope.newTransaction).then(
            function (response){
                getAllAccounts();
                if ($scope.selectedAccount){
                    AccountTransactions($scope.selectedAccount);
                }
                $scope.errors.createTransaction = []
            },
            function (response) {
                $scope.errors.createTransaction = GettAPIErrorMessage(response)
            })
        }
    }
    
})();