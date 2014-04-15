/**
 * Created by icejoywoo on 14-4-15.
 */

var app = angular.module('myApp', []);

app.run(function ($rootScope) {
    $rootScope.name = "icejoywoo";
});
