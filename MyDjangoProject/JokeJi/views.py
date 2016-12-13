from django.views.decorators.cache import cache_page
from django.shortcuts import render_to_response
from django.http import HttpResponse
from JokeJi.models import jokeji
from JokeJi.api import UrlDeal

urldeal = UrlDeal()


def url2data(url_path):
    cont = urldeal.getHtml(url_path)
    urls, data = urldeal.parser(url_path, cont)
    return data


@cache_page(60 * 30)
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
    urlpath = data[index - 1]['urlpath']
    piece = {}
    if index < len(data):
        piece['next'] = {'index': index + 1, 'tittle': data[index]['tittle']}
    if index > 1:
        piece['previous'] = {'index': index - 1, 'tittle': data[index - 2]['tittle']}
    sql_joke = jokeji.objects.filter(urlpath=urlpath)
    if sql_joke:
        jokes = sql_joke.values()[0]
    else:
        jokes = url2data(urlpath)
        jokeji.objects.create(**jokes)
    return render_to_response('index.html', {'joke': jokes, 'l_jokes': data, 'piece': piece, 'l_page': page})
