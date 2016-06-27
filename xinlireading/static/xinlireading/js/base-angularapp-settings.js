var app = angular.module('app', []);
app.config(function($httpProvider, $interpolateProvider) {
  // csrftoken for django.
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  // django and argular use the same '{{' tag, so need to change one to '{%'.
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});
