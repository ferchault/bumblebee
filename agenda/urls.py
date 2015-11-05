# django imports
from django.conf.urls import patterns, url, include

# app-specific imports
from agenda import views

# rest API imports
from rest_framework import routers

urlpatterns = patterns('',
	url(r'^$', views.ProjectListing.as_view(), name='index'),
	url(r'^project/$', views.ProjectListing.as_view(), name='agenda-project-list'),
	url(r'^project/add$', views.ProjectCreate.as_view(), name='agenda-project-add'),
	url(r'^project/edit/(?P<pk>\d+)/$', views.ProjectUpdate.as_view(), name='agenda-project-edit'),
	url(r'^project/delete/(?P<pk>\d+)/$', views.ProjectDelete.as_view(), name='agenda-project-delete'),
)