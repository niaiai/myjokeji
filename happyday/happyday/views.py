from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import datetime
import happyday.jokeji
from django.shortcuts import render_to_response

def joke(request):
	html = happyday.jokeji.jokeMain()
	return HttpResponse(html)

def hello(request):
	return HttpResponse("<h1>Hello, World, I am boy</h1>")

def hours_ahead(request, offset):
	offset = int(offset)
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "<html><body>In %s hour(s), It will be %s. </body></html> "%(offset, dt)
	return HttpResponse(html)

def time(request):
	nowtime = datetime.datetime.now()
	# html = "<html><body>Now is %s. </body></html> "%nowtime
	t = get_template('current_datetime.html')
	html = t.render((Context({'current_date': nowtime})))
	return HttpResponse(html)

def headers(request):
	pass