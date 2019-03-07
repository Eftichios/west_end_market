from django.conf.urls import url
from west_end_market import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addlisting/$', views.add_listing, name='add_listing'),
    #url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    #url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^user/$', views.user_profile, name='user_profile')
    #url(r'^mylistings/$', views.my_listings, name='my_listings'),
    #url(r'^listing/$', views.show_listing, name='show_listing')
]
