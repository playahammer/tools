#coding:utf-8

import requests
from lxml import etree
from selenium.webdriver import Chrome
from base64 import b64decode
import time
import hashlib
from tqdm import tqdm
import argparse

headers = {
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3968.0 Safari/537.36"

}

max_wait_times = 6 # Max waiting time is 60 sec


def byte2hex(b):
    hex_alpha = '0123456789abcdef'
    value = []
    for bb in b:
        value += [hex_alpha[bb // 16], hex_alpha[bb % 16]]
    return ''.join(value)

def main(target_url, target_file=None):

    try:
        print('[+] Getting page from website %s' % target_url)
        browser = Chrome()
        browser.get(target_url)

        video_ele = None
        count = 0
        while not video_ele and count < max_wait_times:
            tree = etree.HTML(browser.page_source)
            video_ele = tree.xpath('//video[@src]')
            time.sleep(10)
            count += 1

        if not video_ele:
            print('[-] Video element is not found in this web page')
            browser.close()
            return

        print('[+] Video element found %s' % video_ele)
        video_src = video_ele[0].attrib.get('src')

        if not video_src:
            print('[-] Video element\'s src attribute not found')
            browser.close()
            return

        video_src = video_src if not video_src.startswith('//') else 'https:' + video_src
        print('[+] Video src is %s' % video_src)

        r = requests.get(video_src, headers=headers,stream=True)
        if r.headers.get('Content-Type') != 'video/mp4':
            print('[-] Response is not video')
            browser.close()
            return

        content_md5 = byte2hex(b64decode(r.headers.get('Content-MD5')))
        content_len = int(r.headers.get('Content-Length')) // 8
        print('[+] The Video file original md5 is %s' % content_md5)
        print('[+] File size %d bytes' % content_len)

        file_md5 = hashlib.md5()

        target_file = target_file if target_file else content_md5 + '.mp4'
        print('[+] File saved to %s' % target_file)

        print('[+] Start to download file')
        with open(target_file, 'wb') as f, tqdm(desc='[+] Downloading',
                                               total=int(content_len),
                                               unit='byte') as bar:
            for chunk in r.iter_content(chunk_size=512):
                if chunk:
                    file_md5.update(chunk)
                    f.write(chunk)
                    bar.update(len(chunk) // 8)

        print('[+] Download Success')
        cal_md5 = file_md5.hexdigest()
        print('[+] Calculating downloaded file md5 %s, md5 is %s'
              % (cal_md5,
                 'match' if cal_md5 == content_md5 else 'mismatch'))
        print('[+] All operation done!')
        browser.close()
        
    except Exception as e:
        print('[-] Error: {}'.format(e))






if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='video page url', type=str)
    parser.add_argument('-o', help='the file path you saved')
    args = parser.parse_args()
    main(args.url, args.o)
