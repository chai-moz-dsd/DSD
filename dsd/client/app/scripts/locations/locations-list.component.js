
angular.module('chaiApp').
  component('locationsList', {
    templateUrl: 'static/locations/locations-list.component.html',
    controller: function() {
      this.locations = [
        {
          name: 'Xian',
          snippet: 'The capital of shaanxi province.'
        },
        {
          name: 'Baoji',
          snippet: 'The second biggest city in shaanxi.'
        }
      ];
    }
  });
