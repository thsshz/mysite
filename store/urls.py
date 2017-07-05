from django.conf.urls import url
from . import views
from . import allstore

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^store/([1-9][0-9]*)$', views.store, name='store'),
    url(r'^create$', views.create, name='create'),
    url(r'^create1$', views.add_alldata, name='add_alldata'),
    url(r'^delete$', views.delete_alldata, name='delete_alldata'),
    url(r'^store/([1-9][0-9]*)/write-review$', views.write_review, name='write_review'),
    url(r'^store/([1-9][0-9]*)/review/sort', views.review_sort, name='review_sort'),
    url(r'^store/([1-9][0-9]*)/review$', views.review, name='review'),
    url(r'^store/([1-9][0-9]*)/review/star/([1-5]0)/sort$', views.review_star_sort, name='review_star_sort'),
    url(r'^store/([1-9][0-9]*)/review/star/([1-5]0)$', views.review_star, name='review_star'),
    url(r'^filter$', allstore.filter, name='filter'),
    url(r'^load_area_category$', views.load_area_category, name='load_area_category'),
    url(r'^area/([1-9][0-9]*)$', views.area_index, name='area_index'),
    url(r'^category/([1-9][0-9]*)$', views.category_index, name='category_index'),
]
