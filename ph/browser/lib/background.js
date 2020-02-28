"use strict"

var values = {}

chrome.runtime.onConnect.addListener(function(port){
      if (port.name == "se23kknsef"){
            port.onMessage.addListener(function(message, sender, sendResponse){
                  console.log(message)
                  if (message.cmd === "push"){
                        var items = message['data'] || []
                        values[sender.sender.tab.id] = items
                  }
                  else if(message.cmd == "pull"){
                        var queryTabId = message.tabId 
                        port.postMessage({cmd: "pull", data: values[queryTabId]})
                  }
            })
      }
})
