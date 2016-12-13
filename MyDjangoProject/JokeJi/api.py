from datetime import datetime, timezone, timedelta
import urllib.parse
import re
import requests
from bs4 import BeautifulSoup


class UrlDeal():
    def __init__(self):
        self.sess = requests.session()
        self.urlRe = re.compile(r'/jokehtml/\w+/\d+\.htm')
        self.tz_8 = timezone(timedelta(hours=8))

    def getHtml(self, url_path):
        url = urllib.parse.urljoin('http://www.jokeji.cn/', url_path)
        html = self.sess.get(url)
        if html.status_code != 200:
            return None
        html.encoding = 'gb18030'
        return html.text

    def _GetNewUrls(self, PageUrl, soup):
        NewUrls = set()
        links = soup.find_all('a', href=self.urlRe)
        for link in links:
            NewUrl = link['href']
            NewUrls.add(NewUrl)
        return NewUrls

    def __Url2date(self, PageUrl):
        tim = PageUrl.split('/')[-1].split('.')[0]
        try:
            if len(tim) < 14:
                update = datetime.strptime(tim[:8], "%Y%m%d").replace(tzinfo=self.tz_8)
            else:
                update = datetime.strptime(tim[:14], "%Y%m%d%H%M%S").replace(tzinfo=self.tz_8)
        except:
            update = datetime.now()
        return update

    def _GetNewData(self, PageUrl, soup):
        ReaData = {'urlpath': PageUrl, 'update': self.__Url2date(PageUrl)}
        try:
            if 'yuanchuangxiaohua' in PageUrl:
                TitleNode = soup.find('div', class_="txt").find("h1")
                ReaData['tittle'] = TitleNode.get_text()
                JokeNode = soup.find('div', class_="txt").find("ul").find('li')
                ReaData['joke'] = JokeNode.get_text() + '\n'
            else:
                SpanNode = soup.find('span', id="text110")
                PNode = SpanNode.find_all("p")
                if PNode:
                    joke = ''
                    for pNode in PNode:
                        joke += pNode.get_text() + '\n'
                else:
                    fontNode = SpanNode.find('font', size='4')
                    joke = fontNode.get_text()
                ReaData['joke'] = joke
                TitleNode = soup.find('div', class_="left_up").find("h1")
                Title = TitleNode.get_text()
                ReaData['tittle'] = Title[Title.find('>', 5) + 2:]
            return ReaData
        except:
            print('error')
            return

    def index(self, page):
        data = []
        if page > 1:
            url_path = 'list_%s.htm' % page
        else:
            url_path = 'list.htm'
        html = self.getHtml(url_path)
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find('div', class_='list_title').find_all(
            'a', href=self.urlRe)
        for link in links:
            data.append({'urlpath': link['href'], 'tittle': link.get_text()})
        return data

    def zw_page(self, soup):
        zw_page1 = soup.find('div', class_='zw_page1').find('a')
        zw_page2 = soup.find('div', class_='zw_page2').find('a')
        pages = {}
        if zw_page1:
            pages['zw_page1'] = [zw_page1['href'], zw_page1.get_text()]
        if zw_page2:
            pages['zw_page2'] = [zw_page2['href'], zw_page2.get_text()]
        return pages

    def parser(self, PageUrl, HtmlCont):
        if PageUrl is None or HtmlCont is None:
            return
        HtmlCont = HtmlCont.replace('<BR>', '\n')
        soup = BeautifulSoup(HtmlCont, 'html.parser')
        PageUrl = urllib.parse.urlparse(PageUrl).path
        # print(soup)
        NewUrls = self._GetNewUrls(PageUrl, soup)
        NewData = self._GetNewData(PageUrl, soup)
        # pages = self.zw_page(soup)
        return NewUrls, NewData
