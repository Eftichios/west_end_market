from django.conf.urls import url, include
from west_end_market import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_listing/$', views.add_listing, name='add_listing'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    #url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^user/(?P<username>[a-zA-Z0-9]+)$', views.user_profile, name='user_profile'),
    #url(r'^my_listings/$', views.my_listings, name='my_listings'),
    #url(r'^listing/$', views.show_listing, name='show_listing'),
    url(r'^auth/', include('social_django.urls', namespace='social')),  #google/facebook
]
