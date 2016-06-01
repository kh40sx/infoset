var app = angular.module('infoset', [], function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('InfosetController', ['$scope', '$http',
   function ($scope, $http) {
     $scope.getHosts = function () {
       $http({ method: 'GET', url: '/hosts' })
       .then(function success(result) {
         $scope.data = result.data;
       },

       function error(err) {
         console.log(err);
       });
     };
   },
]);

