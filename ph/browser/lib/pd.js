'use strict';






(function(){
      MG_Utils.domReady(function(){
            console.debug('dom ready');
            for(var attr in window){
                  if (attr.indexOf('qualityItems') !== -1){
                        var values = window[attr]
                        window.postMessage({id: 'nuh43njwjer0234c', value: values, type: "FROM_PAGE"}, "*")
                        break
                  }
            }           
      })

})();



