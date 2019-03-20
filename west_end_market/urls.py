from django.conf.urls import url, include
from west_end_market import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_listing/$', views.add_listing, name='add_listing'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    #url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^user/(?P<user_username>[\w\-]+)/$', views.user_profile, name='user_profile'),
    #url(r'^my_listings/$', views.my_listings, name='my_listings'),
    url(r'^listing/(?P<listing_id>[\w\-]+)/$', views.show_listing, name='show_listing'),
    url(r'^search_results/$', views.search_results, name='search_results'),
    url(r'^category/(?P<category_title>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^auth/', include('social_django.urls', namespace='social')),  #google/facebook
]
