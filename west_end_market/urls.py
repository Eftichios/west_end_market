from django.conf.urls import url
from west_end_market import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_listing/$', views.add_listing, name='add_listing')
]
