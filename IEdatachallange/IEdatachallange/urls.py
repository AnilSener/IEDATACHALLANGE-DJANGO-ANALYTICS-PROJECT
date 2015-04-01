from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import RedirectView
from hotelapp import views
from hotelapp.view import home

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IEdatachallange.view.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'views.home', name='home'),
    url(r'^hotelapp/$',views.login_view,name='login'),
    url(r'^hotelapp/home/$',views.main, name='main'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hotelapp/get-hotels/$', views.getHotel, name='get_hotels'),
    url(r'^hotelapp/get-attractions/$', views.getAttraction, name='get_attractions'),
    url(r'^hotelapp/get-population/$', views.getPopulation, name='get_population'),
    url(r'^hotelapp/get-graphedges/$',views.getGraphEdges, name='get_graphedges'),
    url(r'^hotelapp/get-hotelsentiment/$',views.getHotelSentimentResults, name='get_hotelsentiment')
)