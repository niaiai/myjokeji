from django.conf.urls import url, include
from django.contrib import admin
from happyday import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^time/$', views.time),
    url(r'^jokeji/$', views.joke),
    url(r'^time/plus/(\d+)/$', views.hours_ahead),
    url(r'^joke/', include('jokeji.urls')),
    url(r'^$', views.hello),
]
