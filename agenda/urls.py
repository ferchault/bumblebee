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
)