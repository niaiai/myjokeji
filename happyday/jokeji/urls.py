from django.conf.urls import url
from jokeji import views

urlpatterns = [
    url(r'^joke/$', views.sqljoke),
    url(r'^header/$', views.header),
    url(r'^search/$', views.search),
    url(r'^gettest/$',views.gettest),
    url(r'^$', views.helloworld),
]