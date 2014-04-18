/**
 * Created by icejoywoo on 14-4-15.
 */

var app = angular.module('myApp', []);

app.run(function ($rootScope) {
    $rootScope.name = "icejoywoo";
});

app.controller('MyController', function($scope) {
    $scope.person = {
        name: "icejoywoo"
    }
});

app.controller('ParentController', function($scope) {
  $scope.person = {greeted: false};
});

app.controller('ChildController', function($scope) {
  $scope.sayHello = function() {
    $scope.person.greeted = true;
  }
});
