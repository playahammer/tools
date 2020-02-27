function injectCustomJS(jsPath)
{
      jsPath = jsPath || 'lib/pd.js';
      var temp = document.createElement('script');
      temp.setAttribute('type', 'text/javascript');
      temp.src = chrome.extension.getURL(jsPath);
      document.head.appendChild(temp);
}

injectCustomJS();


window.addEventListener("message", function(event){
      if (event.source != window)
            return;
      
      if (event.data.type && (event.data.type == "FROM_PAGE")){
            let data = event.data;
            if (data.id === 'nuh43njwjer0234c'){
                  /**
                   * Passing the message to the popup per 0.6 sec 
                   */
                  window.setInterval(
                        chrome.runtime.sendMessage, 600, {data: data.value}, function(response){
                              // Noting to do
                        }
                  );
            }
      }
}, false);

