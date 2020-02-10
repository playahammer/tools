'use strict';






(function(){


      MG_Utils.domReady(function(){
            console.debug('dom ready');
            
            createElement(document.head, 
                  'link', 
                  [{
                        key: 'href', 
                        value:'//cdnjs.cloudflare.com/ajax/libs/mdui/0.4.3/css/mdui.min.css'
            },{
                  key: 'rel',
                  value: 'stylesheet'
            }]);
            createElement(document.head,
                  'script',
                  [{
                        key: 'src',
                        value: '//cdnjs.cloudflare.com/ajax/libs/mdui/0.4.3/js/mdui.min.js'
            }])

            createElement(document.body,
                  'div',
                  [{
                        key: 'id',
                        value: 'pornhub-video-download-xxx',
                  },{
                        key: 'style',
                        value: 'position: relative'
                  }])
            
            createElement(document.body,
                  'div',
                  [{
                        key: 'id',
                        value: 'download-dialog-container'
                  }])
            createElement(document.body,
                  'input',
                  [{
                        key: 'id',
                        value: 'donwload-link-input'
                  },{
                        key: 'style',
                        value: 'display: none'
                  }])
            const floatButton = '<button class="mdui-fab mdui-fab-fixed mdui-color-pink-accent mdui-ripple" style="z-index:999" id="download-dialog-open"> \
            <i class="mdui-icon material-icons">&#xe2c4;</i></button>';
            var fb = document.getElementById('pornhub-video-download-xxx');
            fb && (fb.innerHTML = floatButton);

            var dd = document.getElementById('download-dialog-container');

            
            var trs = '';
            for(var attr in window){
                  if (attr.indexOf('qualityItems') !== -1){
                        var values = window[attr];
                        
                        values.forEach((v, i)=>{
                              var id = 'll-select' + i;
                              const link = '<input  class="mdui-textfield-input" type="text" readonly id="' + id +  '" style="border:none" value="' + v['url'] +'"/>'
                              trs += '<tr>\
                                    <td>' + v['id'] + '</td> \
                                    <td>' + v['text'] + '</td> \
                                    <td>' + link + '</td> \
                                    <td><a href="' + v['url'] + '" download="' + v['url'].split('/').pop().split('?')[0] +
                                          '">'+ '下载</a> <a href="javascript:doCopy(\''+ id +'\')">复制</a></td>\
                                    </tr>' 
                        })
                  }
            }
            
            console.log(trs);
            const table = '<div class="mdui-table-fluid"> \
                  <table class="mdui-table">\
                        <thead>\
                              <th>Id</th>\
                              <th>Text</th>\
                              <th>Url</th>\
                              <th>操作</th>\
                        </thead>\
                        <tbody>\
                              ' + trs + ' \
                        </tbody>\
                  </table>\
                  </div>'
            const downloadDialog = '<div class="mdui-dialog" id="download-dialog"> \
                  <div class="mdui-dialog-title">视频下载</div> \
                  <div class="mdui-dialog-content">' + table + '</div> \
                  <div class="mdui-dialog-actions"> \
                        <button class="mdui-btn mdui-ripple" mdui-dialog-cancel>退出</button>\
                  </div>';
            dd && (dd.innerHTML= downloadDialog)
            
            document.getElementById('download-dialog-open').addEventListener('click', function(){
                  new mdui.Dialog('#download-dialog').open();
            })
      })

      function createElement(parent, type, attrs){
            var ele = document.createElement(type);
            attrs.forEach(attr => {
                  ele.setAttribute(attr.key, attr.value);
            });
            
            parent.appendChild(ele);
      }
      
     

})();


function doCopy(target) {
      var e = document.getElementById(target);
      e && e.select()
      document.execCommand('copy');
      mdui.snackbar({
            message: 'Copy success!!!',
            position: 'right-top'
          });
}