# django imports
from django.conf.urls import patterns, url, include

# app-specific imports
from agenda import views

# rest API imports
from rest_framework import routers

urlpatterns = patterns('',
	url(r'^overview$', views.overview, name='index'),
	url(r'^project/$', views.ProjectListing.as_view(), name='agenda-project-list'),
	url(r'^project/add$', views.ProjectCreate.as_view(), name='agenda-project-add'),
	url(r'^project/edit/(?P<pk>\d+)/$', views.ProjectUpdate.as_view(), name='agenda-project-edit'),
	url(r'^project/delete/(?P<pk>\d+)/$', views.ProjectDelete.as_view(), name='agenda-project-delete'),
	url(r'^status/$', views.StatusListing.as_view(), name='agenda-status-list'),
	url(r'^status/add$', views.StatusCreate.as_view(), name='agenda-status-add'),
	url(r'^status/edit/(?P<pk>\d+)/$', views.StatusUpdate.as_view(), name='agenda-status-edit'),
	url(r'^status/delete/(?P<pk>\d+)/$', views.StatusDelete.as_view(), name='agenda-status-delete'),
	url(r'^priority/$', views.PriorityListing.as_view(), name='agenda-priority-list'),
	url(r'^priority/add$', views.PriorityCreate.as_view(), name='agenda-priority-add'),
	url(r'^priority/edit/(?P<pk>\d+)/$', views.PriorityUpdate.as_view(), name='agenda-priority-edit'),
	url(r'^priority/delete/(?P<pk>\d+)/$', views.PriorityDelete.as_view(), name='agenda-priority-delete'),
	url(r'^entry/$', views.EntryListing.as_view(), name='agenda-entry-list'),
	url(r'^entry/add$', views.EntryCreate.as_view(), name='agenda-entry-add'),
	url(r'^entry/edit/(?P<pk>\d+)/$', views.EntryUpdate.as_view(), name='agenda-entry-edit'),
	url(r'^entry/delete/(?P<pk>\d+)/$', views.EntryDelete.as_view(), name='agenda-entry-delete'),
)