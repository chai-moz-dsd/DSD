angular.
  module('chaiApp').
  config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });


    $routeProvider.
      when('/dieases', {
        template: '<diease-list></diease-list>'
      }).
      when('/locations', {
        template: '<locations-list></locations-list>'
      }).
      otherwise('/');

  }]);
