# django imports
from django.conf.urls import patterns, url, include

# app-specific imports
from results import views

# rest API imports
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'system', views.SystemViewSet)

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^api/', include(router.urls)),
)