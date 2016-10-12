# -*- coding:utf-8 -*-
import re
import requests

urlRe = re.compile(r'/jokehtml/\w+/\d+\.htm')
aRe = re.compile(r'<a.*</a>', re.I)
# <A href="http://www.jokeji.cn/yuanchuangxiaohua/?hyname=%C0%EE%C9%DC%CD%FA" target=_blank>@李绍旺</A>
def jokeMain():
	url_root = 'http://www.jokeji.cn/'
	hadjoke = ''
	rootHtml = getHtml(url_root)
	urls = getUrl(rootHtml)
	for url in urls:
		url = 'http://www.jokeji.cn' + url
		html = getHtml(url)
		havejoke = getJoke(html)
		# print(url, havejoke)
		hadjoke += havejoke
	return hadjoke


def getHtml(url):
	html = requests.get(url)
	html.encoding = 'gb2312'
	if html.status_code != 200:
		return None
	return html.text


def getUrl(html):
	# <div class="newcontent l_left"> <a href="/jokehtml/bxnn/2016042211424719.htm" target="_blank">逗B爆笑,笑声阵阵心情好</a>(3375)<span>2016-4-22</span><span><img src="/images/new.gif" height="11" border="0" width="28"></span></li><li><img src="/images/d02.gif" height="10" border="0" width="8"> <a href="/jokehtml/ert/201604221140223.htm" target="_blank">囧爆家长的恼人熊孩子</a>(1883)<span>2016-4-22</span><span><img src="/images/new.gif" height="11" border="0" width="28"></span></li><li><img src="/images/d02.gif" height="10" border="0" width="8"> <a href="/jokehtml/冷笑话/2016042211392784.htm" target="_blank">高冷的滑稽笑段</a>(1675)<span>2016-4-22</span><span><img src="/images/new.gif" height="11" border="0" width="28"></span></li><li><img src="/images/d02.gif" height="10" border="0" width="8"> <a href="/jokehtml/bxnn/2016042023371366.htm" target="_blank">情侣幽默,恋爱不止,笑料不断</a>(10309)<span>2016-4-20</span><span><img src="/images/new.gif" height="11" border="0" width="28"></span></li><li><img src="/images/d02.gif" height="10" border="0" width="8"> <a href="/jokehtml/bxnn/2016042023324636.htm" target="_blank">污友的搞笑新段儿</a>(6133)<span>2016-4-20</span><span><img src="/images/new.gif" height="11" border="0" width="28"></span></li><li><img src="/images/d02.gif" height="10" border="0" width="8"> <a href="/jokehtml/冷笑话/201604202328055.htm" target="_blank">逗B的荒诞冷段儿</a>(5461)<span>2016-4-20</span><span><img src="/images/new.gif" height="11" border="0" width="28"></span></li><li><img src="/images/d02.gif" height="10" border="0" width="8"> <a href="/jokehtml/bxnn/2016041923450998.htm" target="_blank">爆冷二货,岂能不乐</a>(12116)<span>2016-4-19</span><span><img src="/images/new.gif" height="11" border="0" width="28"></span></li><li><img src="/images/d02.gif" height="10" border="0" width="8"> <a href="/jokehtml/mj/201604192343201.htm" target="_blank">幽默小讽刺,有木有讽到你?</a>(7826)<span>2016-4-19</span><span><img src="/images/new.gif" height="11" border="0" width="28"></span></li><li><img src="/images/d02.gif" height="10" border="0" width="8"> <a href="/jokehtml/ym/2016041922511428.htm" target="_blank" title="笑话集原创笑话精品展第109期">笑话集原创笑话精品展第1...</a>(7594)<span>2016-4-19</span><span><img src="/images/new.gif" height="11" border="0" width="28"></span></li><li><img src="/images/d02.gif" height="10" border="0" width="8"> <a href="/jokehtml/mj/2016041823220419.htm" target="_blank">有点看不懂的搞笑趣事</a>(9846)<span>2016-4-18</span></li>
	start = html.find("newcontent l_left")
	end = html.find('/div', start, -1)
	html = html[start: end]
	return urlRe.findall(html)

def getJoke(html):
	# <span id="text110"></span>
	start = html.find('id="text110">')
	end = html.find('</span>', start, -1)
	html = html[start+13: end]
	aAll = aRe.findall(html)
	for a in aAll:
		html = html.replace(a, '')
	return html
