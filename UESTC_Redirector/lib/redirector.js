"use strict";

(function(){

      const baseLoginUrl = "https://idas.uestc.edu.cn/authserver/login"; 
      const baseIdaMainUrl = "https://idas.uestc.edu.cn/authserver/index.do"
      const baseLoginOutUrl = "https://idas.uestc.edu.cn/authserver/logout"
      let redirectUrlsTracker = new Array();   

      chrome.webRequest.onHeadersReceived.addListener(
            function(details) {
                  if (details.statusCode === 302) {
                        if (redirectUrlsTracker[details.tabId] === undefined)
                              redirectUrlsTracker[details.tabId] = { status: 'Pending', data: new Array(details.url) };
                        
                        // console.log(redirectUrlsTracker[details.tabId])
                        let searchIndex = 0;
                        
                        for (searchIndex = 0; 
                              redirectUrlsTracker[details.tabId].data[searchIndex] !== details.url && searchIndex < redirectUrlsTracker[details.tabId].data.length;
                              searchIndex++);
                        
                        // Found
                        if (searchIndex !== redirectUrlsTracker[details.tabId].data.length) {
                  
                              let location = undefined;
                              details.responseHeaders && details.responseHeaders.forEach(function(e) {
                                    if (e.name && e.name === "Location")
                                          location = e.value;
                                         
                              });

                              if (!location || redirectUrlsTracker[details.tabId].status === "Completed") return details.responseHeaders;

                              if (location.startsWith("http")) 
                                    redirectUrlsTracker[details.tabId].data.push(location);
                              else
                                    redirectUrlsTracker[details.tabId].data.push(new URL(location, details.url).href);
                  
                              if (location.startsWith(baseLoginUrl)) 
                                    redirectUrlsTracker[details.tabId].status = "Completed";
                        }

                  }
                  
                  return details.responseHeaders
            },
            {urls: ["<all_urls>"]},
            ["blocking","responseHeaders"]
      );
      
      chrome.webRequest.onBeforeRequest.addListener(
            function(details) {
                  if (details.url.startsWith(baseLoginOutUrl)) {
                        // console.log(details);
                        chrome.tabs.get(details.tabId, function(tab){
                              delete redirectUrlsTracker[tabId];
                              redirectUrlsTracker[tabId] = {
                                    status: "Pending", 
                                    data: new Array(tab.url, details.url)
                              };
                        })
                  }
            },
            {urls: ["<all_urls>"]}
      )
      chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
            if (redirectUrlsTracker[tabId] === undefined || !changeInfo.url)
                  return;

            if (changeInfo.url.startsWith(baseLoginUrl)) {
                  let redirectLoginUrl = baseLoginUrl + "?redirect=" + redirectUrlsTracker[tabId].data[0];
                  // console.log(redirectUrlsTracker[tabId])
                  chrome.tabs.update(tabId, {url: redirectLoginUrl}, function(_) {
                        console.log("Modify url of top frame");
                  })
            }
            else if (changeInfo.url.startsWith(baseIdaMainUrl)) {
                  console.log("Redirecting to " + redirectUrlsTracker[tabId].data[0]);
                  chrome.tabs.executeScript(
                        tabId,
                        {
                              code: `if (window) window.top.location.href = "${redirectUrlsTracker[tabId].data[0]}"`
                        }, 
                        function(_) {
                              delete redirectUrlsTracker[tabId];
                              console.log("Redirect success!!!");
                        }
                  );
            }
      })
})();