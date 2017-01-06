from django.conf.urls import url
from Grap import views


urlpatterns = [
    url(r'^page_(\d+)/grap_(\d+)$', views.show),
    url(r'^', views.show),
]
