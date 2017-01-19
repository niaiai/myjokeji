from django.conf import settings
from datetime import datetime, timezone, timedelta
import os
import urllib.parse
import re
import requests
from bs4 import BeautifulSoup


class UrlDeal():
    def __init__(self):
        self.sess = requests.session()
        self.media = settings.MEDIAFILES_DIRS[0]
        self.urlRe = re.compile(r'/GrapHtml/\w+/\d+\.htm')
        self.imgRe = re.compile(r'/UpFiles\w*/\d+/\d+/\d+/\d+\.\w+')
        self.tz_8 = timezone(timedelta(hours=8))
        self.imgHeader = {
            'Accept': 'image/webp,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'gaoxiao.jokeji.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.htmlHeader = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'gaoxiao.jokeji.cn',
            'Referer': 'http://gaoxiao.jokeji.cn/GrapHtml/quweigaoxiao/20170111222341.htm',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', }

    def getHtml(self, url_path):
        url = urllib.parse.urljoin('http://gaoxiao.jokeji.cn/', url_path)
        html = self.sess.get(url, headers=self.htmlHeader)
        if html.status_code != 200:
            return None
        html.encoding = 'gb18030'
        return html.text

    def getImg(self, path, referer):
        file_path = os.path.join(self.media, path[1:])
        if os.path.exists(file_path):
            return
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        url = urllib.parse.urljoin('http://gaoxiao.jokeji.cn/', path)
        self.imgHeader['Referer'] = urllib.parse.urljoin(
            'http://gaoxiao.jokeji.cn/', referer)
        r = self.sess.get(url, headers=self.imgHeader, stream=True)
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            f.close()

    def _GetNewUrls(self, PageUrl, soup):
        NewUrls = []
        lsit_lists = soup.find('div', class_='listpic').find_all(
            'div', class_='list_list')
        for list_list in lsit_lists:
            link = list_list.find('a', href=self.urlRe)
            NewUrls.append({'urlpath': link['href'], 'title': link[
                'title'], 'update': self.__Url2date(link['href'])})
        return NewUrls

    def __Url2date(self, PageUrl):
        tim = PageUrl.split('/')[-1].split('.')[0]
        try:
            if len(tim) < 14:
                update = datetime.strptime(
                    tim[:8], "%Y%m%d").replace(tzinfo=self.tz_8)
            else:
                update = datetime.strptime(
                    tim[:14], "%Y%m%d%H%M%S").replace(tzinfo=self.tz_8)
        except:
            update = datetime.now()
        return update

    def _GetNewData(self, PageUrl, soup):
        try:
            lis = soup.find('div', class_="pic_pview").find(
                'ul').find_all('li')
            Imglist = []
            for li in lis:
                img = li.find('img', src=self.imgRe)
                ImgData = {'path': img['src'], 'title': img['alt']}
                Imglist.append(ImgData)
            return Imglist
        except:
            print('error')
            return

    def index(self, page):
        data = []
        # http://gaoxiao.jokeji.cn/list/list_1.htm
        url_path = 'list/list_%s.htm' % page
        html = self.getHtml(url_path)
        soup = BeautifulSoup(html, 'html.parser')
        urlsdata = self._GetNewUrls(url_path, soup)
        return urlsdata

    def parser(self, PageUrl, HtmlCont):
        if PageUrl is None or HtmlCont is None:
            return
        HtmlCont = HtmlCont.replace('<BR>', '\n')
        soup = BeautifulSoup(HtmlCont, 'html.parser')
        PageUrl = urllib.parse.urlparse(PageUrl).path
        imglist = self._GetNewData(PageUrl, soup)
        return imglist
