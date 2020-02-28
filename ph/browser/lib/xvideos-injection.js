'use strict';

(function(){
      window.onload = function(){
            for(var attr in window){
                  if (attr == "html5player"){
                        var values = [{
                              text: "高品质",
                              url: window[attr].url_high
                        },{
                              text: "低品质",
                              url: window[attr].url_low
                        }]
                        window.postMessage({id: 'nuh43njwjer0234c', value: values, type: "FROM_PAGE"}, "*")
                        break
                  }
            }
      }
})()