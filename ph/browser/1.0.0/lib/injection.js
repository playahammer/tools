function injectCustomJS(jsPath)
{
      console.log('Injection js');
      jsPath = jsPath || 'lib/pd.js';
      var temp = document.createElement('script');
      temp.setAttribute('type', 'text/javascript');
      console.log(chrome.extension.getURL(jsPath))
      temp.src = chrome.extension.getURL(jsPath);
      document.head.appendChild(temp);
}

injectCustomJS();


