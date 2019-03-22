from django.conf.urls import url, include
from west_end_market import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_listing/$', views.add_listing, name='add_listing'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^user/(?P<user_username>[\w\-]+)/$', views.user_profile, name='user_profile'),
    url(r'^my_account/$', views.my_account, name='my_account'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^listing/(?P<listing_id>[\w\-]+)/$', views.show_listing, name='show_listing'),
    url(r'^search_results/$', views.search_results, name='search_results'),
    url(r'^search_results/(?P<search>[\w\-]+)/(?P<sort_by>[\w\-]+)/$', views.search_results, name='search_results'),
    url(r'^category/(?P<category_title>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/(?P<category_title>[\w\-]+)/(?P<sort_by>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^edit_listing/(?P<listing_id>[\w\-]+)/$', views.edit_listing, name='edit_listing'),
    url(r'^delete_listing/(?P<pk>[\w\-]+)/$', views.ListingDelete.as_view(), name='delete_listing'),
    url(r'^cookie_policy/$', views.cookie_policy, name="cookie_policy"),
]
