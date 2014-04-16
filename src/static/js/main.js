/**
 * Created by wujiabin on 14-4-15.
 */

// 定义module
var app = angular.module('myApp', []);

app.run(function($rootScope) {
    $rootScope.name = "icejoywoo";
});