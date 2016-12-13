from django.conf.urls import url
from JokeJi import views


urlpatterns = [
    url(r'^page_(\d+)/joke_(\d+)$', views.show),
    url(r'^', views.show),
]
