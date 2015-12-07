# django imports
from django.conf.urls import patterns, url, include

# app-specific imports
from results import views

# rest API imports
from rest_framework_bulk.routes import BulkRouter

router = BulkRouter()
router.register(r'system', views.SystemViewSet)
router.register(r'bucket', views.BucketViewSet)
router.register(r'series', views.SeriesViewSet)
router.register(r'seriesattributes', views.SeriesAttributesViewSet)
router.register(r'singlepoint', views.SinglePointViewSet)
router.register(r'singlepointouter', views.SinglePointOuterViewSet)
router.register(r'singlepointattributes', views.SinglePointAttributesViewSet)
router.register(r'mdrun', views.MDRunViewSet)
router.register(r'mdstep', views.MDStepViewSet)
router.register(r'atom', views.AtomViewSet)
router.register(r'coordinate', views.CoordinateViewSet)
router.register(r'coordinatewrapped', views.CoordinateWrappedViewSet)
router.register(r'hirshfeldcharge', views.HirshfeldChargeViewSet)
router.register(r'scaledcoordinate', views.ScaledCoordinateViewSet)
router.register(r'scaledcoordinatewrapped', views.ScaledCoordinateWrappedViewSet)
router.register(r'mullikencharge', views.MullikenChargeViewSet)
router.register(r'mdrunsettings', views.MDRunSettingsViewSet)
router.register(r'mdrunattributes', views.MDRunAttributesViewSet)
router.register(r'stepcell', views.StepCellViewSet)
router.register(r'stepensemble', views.StepEnsembleViewSet)
router.register(r'stepcontributionsqm', views.StepContributionsQMViewSet)
router.register(r'stepenergy', views.StepEnergyViewSet)
router.register(r'stepmetaqm', views.StepMetaQMViewSet)

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^system/$', views.SystemListing.as_view(), name='results-system-list'),
	url(r'^system/add$', views.SystemCreate.as_view(), name='results-system-add'),
	url(r'^system/show/(?P<pk>\d+)/$', views.show_system, name='results-system-show'),
	url(r'^system/show/(?P<system>\d+)/(?P<bucket>\d+)/$', views.show_bucket, name='results-bucket-show'),
	url(r'^system/show/(?P<system>\d+)/(?P<bucket>\d+)/(?P<series>\d+)/$', views.show_series, name='results-series-show'),
	url(r'^mdrun/delete/(?P<pk>\d+)/$', views.MDRunDelete.as_view(), name='results-mdrun-delete'),
	url(r'^api/', include(router.urls)),
)