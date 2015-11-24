# django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count

# app-specific imports
from results.models import *
from bumblebee.models import *

# rest API imports
from rest_framework import viewsets
from results.serializers import *
from rest_framework import filters
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)
from rest_framework_bulk.generics import BulkModelViewSet


def index(request):
	template = loader.get_template('results/index.html')
	systems = System.objects.all()
	context = RequestContext(request, {
		'systems': systems,
	})
	return render(request, 'results/index.html', context)


class SystemListing(ModelNameMixin, ListView):
	model = System
	template_name = 'listview-generic.html'
	fields = ('name', 'bucket_count')
	queryset = System.objects.annotate(bucket_count=Count('bucket'))


class SystemCreate(ModelNameMixin, CreateView):
	model = System
	form_class = SystemForm
	success_url = reverse_lazy('results-system-list')
	template_name = 'createview-generic.html'


class SystemViewSet(viewsets.ModelViewSet):
	queryset = System.objects.all().order_by('name')
	serializer_class = SystemSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class BucketViewSet(viewsets.ModelViewSet):
	serializer_class = BucketSerializer
	queryset = Bucket.objects.all()
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class SeriesViewSet(viewsets.ModelViewSet):
	queryset = Series.objects.all().order_by('name')
	serializer_class = SeriesSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class SeriesAttributesViewSet(viewsets.ModelViewSet):
	queryset = SeriesAttributes.objects.all()
	serializer_class = SeriesAttributesSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class SinglePointViewSet(viewsets.ModelViewSet):
	queryset = SinglePoint.objects.all()
	serializer_class = SinglePointSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class SinglePointOuterViewSet(viewsets.ModelViewSet):
	queryset = SinglePointOuter.objects.all()
	serializer_class = SinglePointOuterSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class SinglePointAttributesViewSet(viewsets.ModelViewSet):
	queryset = SinglePointAttributes.objects.all()
	serializer_class = SinglePointAttributesSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class MDRunViewSet(viewsets.ModelViewSet):
	queryset = MDRun.objects.all()
	serializer_class = MDRunSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class MDStepViewSet(viewsets.ModelViewSet):
	queryset = MDStep.objects.all()
	serializer_class = MDStepSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class AtomViewSet(viewsets.ModelViewSet):
	queryset = Atom.objects.all()
	serializer_class = AtomSerializer
	filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class CoordinateViewSet(BulkModelViewSet):
	queryset = Coordinate.objects.all()
	serializer_class = CoordinateSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class CoordinateWrappedViewSet(viewsets.ModelViewSet):
	queryset = CoordinateWrapped.objects.all()
	serializer_class = CoordinateWrappedSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class HirshfeldChargeViewSet(viewsets.ModelViewSet):
	queryset = HirshfeldCharge.objects.all()
	serializer_class = HirshfeldChargeSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class ScaledCoordinateViewSet(viewsets.ModelViewSet):
	queryset = ScaledCoordinate.objects.all()
	serializer_class = ScaledCoordinateSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class ScaledCoordinateWrappedViewSet(viewsets.ModelViewSet):
	queryset = ScaledCoordinateWrapped.objects.all()
	serializer_class = ScaledCoordinateWrappedSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class MullikenChargeViewSet(BulkModelViewSet):
	queryset = MullikenCharge.objects.all()
	serializer_class = MullikenChargeSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class MDRunSettingsViewSet(viewsets.ModelViewSet):
	queryset = MDRunSettings.objects.all()
	serializer_class = MDRunSettingsSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class MDRunAttributesViewSet(viewsets.ModelViewSet):
	queryset = MDRunAttributes.objects.all()
	serializer_class = MDRunAttributesSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class StepCellViewSet(viewsets.ModelViewSet):
	queryset = StepCell.objects.all()
	serializer_class = StepCellSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class StepEnsembleViewSet(viewsets.ModelViewSet):
	queryset = StepEnsemble.objects.all()
	serializer_class = StepEnsembleSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class StepContributionsQMViewSet(viewsets.ModelViewSet):
	queryset = StepContributionsQM.objects.all()
	serializer_class = StepContributionsQMSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class StepEnergyViewSet(viewsets.ModelViewSet):
	queryset = StepEnergy.objects.all()
	serializer_class = StepEnergySerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class StepMetaQMViewSet(viewsets.ModelViewSet):
	queryset = StepMetaQM.objects.all()
	serializer_class = StepMetaQMSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])
