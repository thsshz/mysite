from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^create$', views.create, name='create'),
    url(r'^store/([1-9][0-9]*)$', views.store, name='store'),
    url(r'^store/([1-9][0-9]*)/write-review$', views.write_review, name='write_review'),
]