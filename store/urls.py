from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^create$', views.create, name='create'),
    url(r'^store/([1-9][0-9]*)$', views.store, name='store'),
    url(r'^store/([1-9][0-9]*)/reviews', views.review, name = 'review'),
    url(r'^store/([1-9][0-9]*)/write-review$', views.write_review, name='write_review'),
    url(r'^store/([1-9][0-9]*)/review$', views.review, name='review'),
    url(r'^store/([1-9][0-9]*)/review-5star$', views.review_5star, name='review_5star'),
    url(r'^store/([1-9][0-9]*)/review-4star$', views.review_4star, name='review_4star'),
    url(r'^store/([1-9][0-9]*)/review-3star$', views.review_3star, name='review_3star'),
    url(r'^store/([1-9][0-9]*)/review-2star$', views.review_2star, name='review_2star'),
    url(r'^store/([1-9][0-9]*)/review-1star$', views.review_1star, name='review_1star'),
    url(r'^store/([1-9][0-9]*)/review/sort$', views.review_sort, name='review_sort'),
    url(r'^store/([1-9][0-9]*)/review-5star/sort$', views.review_5star_sort, name='review_5star_sort'),
    url(r'^store/([1-9][0-9]*)/review-4star/sort$', views.review_4star_sort, name='review_4star_sort'),
    url(r'^store/([1-9][0-9]*)/review-3star/sort$', views.review_3star_sort, name='review_3star_sort'),
    url(r'^store/([1-9][0-9]*)/review-2star/sort$', views.review_2star_sort, name='review_2star_sort'),
    url(r'^store/([1-9][0-9]*)/review-1star/sort$', views.review_1star_sort, name='review_1star_sort'),
]
