from django.views.decorators.cache import cache_page
from django.shortcuts import render_to_response
from django.http import HttpResponse
from Grap.models import grap, img
from Grap.api import UrlDeal

urldeal = UrlDeal()


def url2data(url_path):
    cont = urldeal.getHtml(url_path)
    data = urldeal.parser(url_path, cont)
    return data


# @cache_page(60 * 30)
def show(request, page=1, index=1):
    page = 1 if not page else page
    index = 1 if not index else index
    try:
        page = int(page)
        index = int(index)
    except:
        return HttpResponse('<h2>ERROR</h2>')
    data = urldeal.index(page)
    if not index or index > len(data):
        index = 1
    # http://gaoxiao.jokeji.cn/list/list_1.htm
    graps = data[index - 1]
    urlpath = data[index - 1]['urlpath']
    piece = {}
    if index < len(data):
        piece['next'] = {'index': index + 1, 'title': data[index]['title']}
    if index > 1:
        piece['previous'] = {'index': index - 1,
                             'title': data[index - 2]['title']}
    sql_grap = grap.objects.filter(urlpath=urlpath)
    if sql_grap:
        imgs = sql_grap[0].img_set.all()
    else:
        imgs = url2data(urlpath)
        index_grap = grap.objects.create(**data[index - 1])
        for i in imgs:
            graps_sql = img.objects.create(grap=index_grap, **i)
    for i in imgs:
        urldeal.getImg(i['path'] if isinstance(i, dict) else i.path, urlpath)
    return render_to_response('index_gif.html', {'graps': graps, 'imgs': imgs, 'data_list': data, 'piece': piece, 'l_page': page})
