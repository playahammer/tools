var values = {};

var Event = {update: null};
var $$ = mdui.JQ;

Event.update = function(){
      chrome.tabs.query({active: true, currentWindow: true}, resultTabs=>{
            var currentTab = resultTabs[0]
            var items = values[currentTab.id] || []
            var innerHTML = ""
            items.forEach((item, index) => {
                  innerHTML += "<tr><td>" + index + "</td><td>" + item.text + "</td><td><button class=\"download mdui-btn\" data-url=\"" + item.url + "\">下载</button></td></tr>"
            });
            
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


      })
}


chrome.runtime.onMessage.addListener(

      function(message, sender, sendResponse){
            var items = message['data'] || []

            
            if (Object.keys(values).indexOf(sender.tab.id.toString()) == -1 || !compare(items, values[sender.tab.id])) {
                  Event.update()
            }
            
            values[sender.tab.id] = items
      }
)

function compare(arr1, arr2){
      console.debug(arr1, arr2)
      if (arr1.length != arr2.length){
            return false
      }

      for(var index = 0; index < arr1.length; index++){
            for (var attr in arr1[index]){
                  if (arr1[index][attr] !== arr2[index][attr])
                        return false
            }
      }
      return true
}



      


