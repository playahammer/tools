#coding:utf-8

import re
import requests
from lxml import etree
from selenium.webdriver import Chrome
import time
import argparse
import hashlib

chapters = re.compile(r'<a\b[^>]*\bhref=[\"|\']([^\"\']*)[\"|\'][^>]*>([^<>]*)</a>', re.I | re.M)
url_prefix = re.compile(r'^https?://.*', re.I| re.M)
script_tag = re.compile(r'<script\b[^>]*>[^<]*</script>')
html_tag = re.compile(r'<[^>]*>', re.I|re.M)
original_url = re.compile(r'^(https?://[^/]*)', re.I|re.M)
enter = re.compile(r'&#13;', re.I|re.M)

TIMEOUT_SEC = 5

# Set user agent header
headers={
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3968.0 Safari/537.36"

}

NAME = '未命名'

def defaultTextName():
    h = hashlib.sha256()
    h.update(str(time.time()).encode('ascii'))
    return h.hexdigest()

class Spider(object):

    def __init__(self, url,
                 using_chrome=False,
                 save_file=None,
                 title=None):
        self._url = url
        self._chapters = []
        self.using_chrome = using_chrome

        if using_chrome:
            self.chrome = Chrome()
        self.save_file = save_file
        self.title = title
        self._f = None


    def run(self):
        self.get_chapters()

        if self.save_file:
            self._f = open(self.save_file, 'w+')
            if self.title:
                self._f.write(self.title + '\n')

        chapter_index = 0
        while chapter_index < len(self._chapters):
            chapter = self._chapters[chapter_index]
            try:
                if self.using_chrome:
                    self.chrome.get(chapter.get('url'))
                    content = self.chrome.page_source
                else:
                    r = requests.get(chapter.get('url'), headers=headers, timeout=TIMEOUT_SEC)
                    r.encoding = Spider.content_encoding(r.text)
                    content = r.text
                html = etree.HTML(content)

                div_content = html.xpath('//div[@id="content"]')
                print(chapter.get('chapter'), chapter.get('name'))
                if div_content:
                    page = etree.tostring(div_content[0], encoding='utf-8').decode('utf-8')
                    page_content = Spider.html_tag_split(page)
                    if self._f and self.save_file:
                        self._f.write('%s %s\n\n\n' % (ChapterParser.to_number(chapter.get('chapter')), chapter.get('name')))
                        self._f.write(page_content + '\n')
                    print(Spider.html_tag_split(page))
                time.sleep(5)
            except Exception as e:
                print(e)
            else:
                chapter_index += 1

        if self._f and not self._f.closed:
                self._f.close()


    @property
    def original_url(self):
        return original_url.findall(self._url)[0]

    @staticmethod
    def content_encoding(text):
        html = etree.HTML(text)
        meta = html.xpath('//meta[@http-equiv="Content-Type"]')
        if meta:
            attr = meta[0].attrib
            if 'gbk' in attr['content']:
                return 'gbk'
            else:
                return 'utf-8'
        return 'utf-8'

    @staticmethod
    def html_tag_split(html):
        # Remove script tag and content
        html = script_tag.sub('', html)
        html = enter.sub('\n', html)
        return html_tag.sub('', html)

    def get_chapters(self):
        try:
            if self.using_chrome:
                self.chrome.get(self._url)
                content = self.chrome.page_source
            else:
                r = requests.get(self._url, headers=headers, timeout=TIMEOUT_SEC)
                r.encoding = Spider.content_encoding(r.text)
                content = r.text

            finder = chapters.findall(content)
            # print(finder)
            for f in finder:
                # print(f)
                if not url_prefix.match(f[0]):  # Fix url
                    if f[0].startswith('/'): # Absolute url path
                        url = self.original_url + f[0]
                    elif not self._url.endswith('/'):
                        url = self._url + '/' + f[0]
                    else:
                        url = self._url + f[0]
                else:
                    url = f[0]
                parser = ChapterParser(f[1])
                name = parser.name
                number = parser.number

                # print((url, name, number))
                if number != 0:
                    self._chapters.append({
                        'chapter': number,
                        'name':name,
                        'url': url
                    })


            for k in self._chapters:
                print(k)
        except Exception as e:
            print(e)
        return self._chapters

    # def __del__(self):
    #     if self.using_chrome:
    #         self.chrome.quit() # Close chrome browser

    def __repr__(self):
        return '<Spider url at "%s">' % self._url



class ChapterParser(object):
    Standard = 1
    Int = 2
    Big = 3

    number_table = {
        '零': 0,
        '0': 0,
        '一': 1,
        '1': 1,
        '二': 2,
        '两': 2,
        '2': 2,
        '三': 3,
        '3': 3,
        '四': 4,
        '4': 4,
        '五': 5,
        '5': 5,
        '六': 6,
        '6': 6,
        '七': 7,
        '7': 7,
        '八': 8,
        '8': 8,
        '九': 9,
        '9': 9,
        '十': 10,
        '百': 100,
        '千': 1000,
        '万': 10000
    }

    max_value = 99999

    skip_words = ':,：。 '

    def __init__(self, chapter):
        self._chapter = chapter
        self._chapter_name = ''
        self._chapter_number = ''
        self.numbers = []
        self._parser()


    def _parser(self):
        if not self._chapter:
            return
        iter_str = StrIterator(self._chapter)
        first_word = next(iter_str)
        if first_word not in self.number_table.keys() and first_word != '第':
            return
        else:
            self._chapter_number += first_word
        while True:
            try:
                word = next(iter_str)
                if word in self.number_table.keys():
                    self._chapter_number += word
                else:
                    break

            except StopIteration:
                return
        self._chapter_number = self._chapter_number[::-1]

        while True:
            try:
                word = next(iter_str)
                if word not in self.skip_words:
                    self._chapter_name += word
            except StopIteration:
                break

        if len(self._chapter_name[0].encode('utf-8')) == 1:
            self._chapter_name = self._chapter_name[1:]

    @property
    def number(self):
        if not self._chapter_number:
            return 0
        try:
            return int(self._chapter_number[::-1])
        except ValueError:
            number = 0
            self.numbers = []
            number_iter = StrIterator(self._chapter_number)
            visited_other = False # If visited 十、百、千、万 is True
            while True:
                try:
                    value = next(number_iter)
                    if value in ['第', '章']:
                        continue
                    else:
                        try:
                            if int(self.number_table[value]) <= 9 and self.number_table[value] >= 0:
                                if visited_other:
                                    self.numbers[len(self.numbers) - 1] = int(self.number_table[value])
                                    visited_other = False
                                else:
                                    self.numbers.append(int(self.number_table[value]))
                            else:
                                bit = ChapterParser.bit_dec(self.number_table[value])
                                while len(self.numbers) < bit - 1:
                                    self.numbers.append(0)
                                self.numbers.append(1)
                                visited_other = True
                        except KeyError:
                            return 0
                except StopIteration:
                    break

            base = 1
            for num in self.numbers:
                number += (num * base)
                base *= 10
            return number

    @staticmethod
    def to_number(int_number, format_type=1):
        if int_number > ChapterParser.max_value:
            raise OutOfMaxValue("Max value: %d, your value is %d" % (ChapterParser.max_value, int_number))

        if int_number == 0:
            raise OutOfMaxValue('Min value: 1, your value is 0')
        if format_type == ChapterParser.Int:
            return str(int_number)

        numbers = []
        while int_number:
            numbers.append(int_number % 10)
            int_number = int(int_number / 10)

        re_number_table = {0: '零', 1: '一',2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九'}

        # 二千八百零四 四零八二 四十零百八千二
        # 二千零四    四零零二 四十零百零千二
        # 二千零一十四 四一零二 四十一百零千二
        # 一万零三    三零零零一 三十零百零千零万一
        # 一百零四    四零一 四十零百一
        values = ''.join(map(lambda x: re_number_table.get(x), numbers))

        if format_type == ChapterParser.Standard:

            flags = ['十', '百', '千', '万']
            new_value = []


            for i in range(len(values) - 1):
                new_value += values[i]
                new_value += flags[i]
            new_value += values[len(values) - 1]


            new_value = new_value[::-1]
            visited = False
            s = 0
            while s < len(new_value):
                if new_value[s] == '零':
                    if not visited:
                        try:
                            new_value.pop(s + 1)
                        except:
                            new_value.pop(s)
                        visited = True
                        s += 1
                    else:
                        try:
                            new_value.pop(s)
                            new_value.pop(s)
                        except IndexError:
                            break

                else:
                    s += 1

            if new_value[len(new_value) - 1] == '零':
                new_value.pop(len(new_value) - 1)

            values = ''.join(new_value[::-1])

        return '第' + values[::-1] + '章'

    @property
    def name(self):
        return self._chapter_name

    @staticmethod
    def bit_dec(dec):
        bit = 0
        while dec:
            dec = int(dec / 10)
            bit += 1
        return bit



    def __len__(self):
        return len(self.numbers)

    def __repr__(self):
        return "<ChapterParser %d, %s>" % (self.number, self.name)

class OutOfMaxValue(Exception):
    pass


class StrIterator(object):

    def __init__(self, str1):
        self.str1 = str1
        self._index = 0

    def __next__(self):
        if self._index >= len(self.str1):
            raise StopIteration
        w = self.str1[self._index]
        self._index += 1
        return w

TRUE_FLAG = ('yes', 'true', 't', 'y', '1')
FALSE_FLAG = ('no', 'false', 'f', 'n', '0')

def strbool(v):
    if v.lower() in TRUE_FLAG:
        return True
    elif v.lower() in FALSE_FLAG:
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='The novel chapter url')
    parser.add_argument('--title', '-t',
                        const=NAME,
                        help="The name of novel")
    parser.add_argument('--output', '-o',
                        const=defaultTextName() + '.txt',
                        help="The file output")
    parser.add_argument('--browser', '-b',
                        nargs='?',
                        type=strbool,
                        const=False,
                        help='Using browser {}, not {}'.format(TRUE_FLAG, FALSE_FLAG))
    parser.add_argument('--verbose', 'v',
                        nargs='?',
                        type=strbool,
                        const=False,
                        help='Printing chapter on the screen {}, not {}'.format(TRUE_FLAG, FALSE_FLAG))

    parser.add_argument('--time', 't',
                        type=int,
                        const=5,
                        help='Each request will wait some time')

    args = parser.parse_args()


    Spider(args.url,
           using_chrome=args.browser,
           save_file=args.output,
           title=args.title).run()
    

