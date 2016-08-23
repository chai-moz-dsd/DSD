
angular.module('chaiApp').
  component('dieaseList', {
    templateUrl: 'static/diease/diease-list.component.html',
    //template: '<html><body><div><p>successfully</p></div></body></html>',
    controller: function() {
      this.dieases = [
        {
          name: 'HIV',
          snippet: 'can spread by sexual behavior'
        },
        {
          name: 'NH2',
          snippet: 'can spread by bird'
        }
      ];
    }
  });
