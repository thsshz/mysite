from django.conf.urls import url
from . import views, allstore, create, auth_views, reviewsearch
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^store/([1-9][0-9]*)$', views.store, name='store'),
    url(r'^create$', views.create, name='create'),
    url(r'^create1$', create.add_alldata, name='add_alldata'),
    url(r'^delete$', create.delete_alldata, name='delete_alldata'),
    url(r'^store/([1-9][0-9]*)/write-review/([1-9][0-9]*)$', views.write_review, name='write_review'),
    url(r'^store/([1-9][0-9]*)/review/sort', views.review_sort, name='review_sort'),
    url(r'^store/([1-9][0-9]*)/review$', views.review, name='review'),
    url(r'^store/([1-9][0-9]*)/review/star/([1-5]0)/sort$', views.review_star_sort, name='review_star_sort'),
    url(r'^store/([1-9][0-9]*)/review/star/([1-5]0)$', views.review_star, name='review_star'),
    url(r'^filter$', allstore.filter, name='filter'),
    url(r'^load_area_category$', views.load_area_category, name='load_area_category'),
    url(r'^area/([1-9][0-9]*)$', views.area_index, name='area_index'),
    url(r'^category/([1-9][0-9]*)$', views.category_index, name='category_index'),
    # auth
    url(r'^login$', auth_views.login, name='login'),
    url(r'^authenticate$', auth_views.authenticate, name='authenticate'),
    url(r'^signup$', auth_views.signup, name='signup'),
    url(r'^signup/submit$', auth_views.signup_submit, name='signup-submit'),
    url(r'^logout$', auth_views.logout, name='logout'),
    url(r'^likestore/([1-9][0-9]*)/([1-9][0-9]*)$', auth_views.likestore, name='likestore'),
    url(r'^client/([0-9][0-9]*)$', auth_views.client, name='client'),
  
    
    url(r'^store/([1-9][0-9]*)/review/match$', views.review_match, name='review_match'),
    url(r'^review_search$', create.search_paragragh, name='search_paragraph'),
]
