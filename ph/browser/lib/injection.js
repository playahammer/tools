function injectCustomJS(jsPath)
{
      jsPath = jsPath || 'lib/pd.js';
      var temp = document.createElement('script');
      temp.setAttribute('type', 'text/javascript');
      temp.src = chrome.extension.getURL(jsPath);
      document.head.appendChild(temp);
}
const pornhub_com_RegExp = /^https?:\/\/[^\/]*\.pornhub\.com/i
const xvideos_com_RegExp = /^https?:\/\/[^\/]*\.xvideos\.com/i

const url = window.location.href

if (pornhub_com_RegExp.test(url)){
      injectCustomJS('lib/pornhub-injection.js')
}
else if (xvideos_com_RegExp.test(url)){
      injectCustomJS('lib/xvideos-injection.js')
}

window.addEventListener("message", function(event){
      if (event.source != window)
            return;
      
      if (event.data.type && (event.data.type == "FROM_PAGE")){
            let data = event.data;
            if (data.id === 'nuh43njwjer0234c'){
                  /**
                   * Passing the message to the popup per 0.6 sec 
                   */
                  
                  this.send({cmd: 'push', data: data.value})
                  
            }
      }
}, false);

this.send = function(msg){
      if(typeof chrome.app.isInstalled !== "undefined"){
            var port = chrome.runtime.connect({name: "se23kknsef"})

            port.onDisconnect.addListener(obj=>{
                  this.setTimeout(send, 600, msg)
            })

            port.postMessage(msg)
      }

}
