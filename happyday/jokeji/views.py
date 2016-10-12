from django.shortcuts import render_to_response
from jokeji.models import jokeji
from django.http import HttpResponse
import datetime
import time

# Create your views here.
one_page = 10

def sqljoke(request):
	c = jokeji.objects.filter(urlpath__contains="20160502")
	# c = str(c).split('@|_|@')
	# print(c[0].joke.replace('\n', '<br>'))
	return render_to_response('jokeji/index.html', {'list': c})

def helloworld(request):
	return HttpResponse("<h1>你好世界，我是jokeji！</h1>")

def header(request):
	# print(request.META)
	agent = request.META.get('HTTP_USER_AGENT', 'unknown')
	if 'Android' in agent:
		OS = 'Android'
	print(agent)
	agent = agent.split('/')
	return render_to_response('jokeji/header.html',{'header':request.META, 'agent':agent})

def search(request):
	today = datetime.date.today().strftime("%Y%m%d")
	today = date_offset(today,-1)
	try:
		curP = int(request.GET.get('curP', 1))
		allP = int(request.GET.get('allP', 1))
		offS = int(request.GET.get('offS', 0))
	except ValueError:
		curP = allP = 1
		offS = 0

	if 'date' in request.GET:
		try:
			date = str(request.GET.get('date',today))
			if not is_valid_date(date):
				date = today
		except:
			date = today
	else:
		date = today

	if offS:
		date = date_offset(date, offS)

	print(date)


	start = (curP - 1) * one_page
	end = start + one_page

	if curP == 1 and allP == 1:
		allP = lookfor_date(date, 1, 1)

	joke = lookfor_date(date, start, end)

	message = 'you searched for %s, curP is %s, allP is %s'%(date, curP, allP)
	print('--->', message)
	return render_to_response('jokeji/search.html',{'joke': joke, 'date':date,'curP':curP, 'allP':allP})


def lookfor_date(date,start,end):
	if start == 1 and end == 1:
		cont = jokeji.objects.filter(urlpath__contains=date).count()
		return (cont + one_page - 1) // one_page
	joke = jokeji.objects.filter(urlpath__contains=date)[start:end]
	return joke


def date_offset(date, offset):
	if is_valid_date(date):
		nowtime = time.strptime(date, "%Y%m%d")
		nowdate = datetime.datetime(*nowtime[:3])
		offset_day = datetime.timedelta(days=offset)
		return (nowdate + offset_day).strftime("%Y%m%d")

def is_valid_date(date):
	try:
		time.strptime(date, "%Y%m%d")
		return True
	except:
		print('False' ,date)
		return False


def gettest(request):



	return render_to_response("jokeji/gettest.html")