var values = {};

var Event = {update: null};
var $$ = mdui.JQ;


window.onload = function(){
      chrome.tabs.query({active: true, currentWindow: true}, resultTabs=>{
            var currentTab = resultTabs[0]
            var port = chrome.runtime.connect({name: "se23kknsef"})

            port.postMessage({cmd: 'pull', tabId: currentTab.id})
            port.onMessage.addListener(message=>{
                  if(message) {
                        var items = message.data
                        var innerHTML = ""
                        items && items.forEach((item, index) => {
                              innerHTML += "<tr><td>" + index + "</td><td>" + item.text + "</td><td><button class=\"download mdui-btn\" data-url=\"" + item.url + "\">下载</button></td></tr>"
                        })
                        
                        document.querySelector("tbody").innerHTML = innerHTML

                        $$('.download').on('click', function(e){
                              var url = e.target.getAttribute('data-url')
                              url && chrome.downloads.download({url: url}, function(id){
                                    mdui.snackbar({
                                          message: '已成功创建下载',
                                          postion: 'right-top',
            
                                    })
                              })
                        })
                  }
            })
           
      })
}
