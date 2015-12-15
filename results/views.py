# django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.views.generic import ListView, CreateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Count

# app-specific imports
from results.models import *
from bumblebee.models import *

# rest API imports
import django_filters
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

def show_system(request, pk):
	try:
		system = System.objects.get(pk=pk)
	except:
		raise Http404('System does not exist.')
	context = RequestContext(request, {
		'object_list': system.bucket_set.all(),
		'system': system,
		'fields': ('name', 'comment', 'updated', 'system'),
	})
	return render(request, 'results/showsystem.html', context)

def show_bucket(request, system, bucket):
	try:
		system = System.objects.get(pk=system)
		bucket = Bucket.objects.get(pk=bucket)
		assert(bucket.system_id == system.id)
	except:
		raise Http404('System or bucket not found.')
	context = RequestContext(request, {
		'object_list': bucket.series_set.all(),
		'system': system,
		'bucket': bucket,
		'fields': ('name', ),
	})
	return render(request, 'results/showbucket.html', context)

def show_series(request, system, bucket, series):
	try:
		system = System.objects.get(pk=system)
		bucket = Bucket.objects.get(pk=bucket)
		series = Series.objects.get(pk=series)
		runs = series.mdrun_set.order_by('part')
		assert(bucket.system_id == system.id)
		assert(series.bucket_id == bucket.id)
	except:
		raise Http404('System, bucket or series not found.')
	context = RequestContext(request, {
		'system': system,
		'bucket': bucket,
		'series': series,
		'runs': runs,
	})
	return render(request, 'results/showseries.html', context)


class LimitUnfilteredQueriesMixin(viewsets.ModelViewSet):
	def get_queryset(self):
		valid_filters = set(self.filter_fields)
		filters_got = set(self.request.query_params.keys())

		if len(filters_got.intersection(valid_filters)) == 0:
			return self.queryset[:10]
		else:
			return self.queryset

	def get_serializer_context(self):
		context = super(LimitUnfilteredQueriesMixin, self).get_serializer_context()
		context['request'] = self.request
		return context


class SystemListing(ModelNameMixin, ListView):
	model = System
	template_name = 'listview-generic.html'
	fields = ('name', 'bucket_count', 'atomic_mass')
	queryset = System.objects.annotate(bucket_count=Count('bucket'))


class SystemCreate(ModelNameMixin, CreateView):
	model = System
	form_class = SystemForm
	success_url = reverse_lazy('results-system-list')
	template_name = 'createview-generic.html'


class SystemDelete(ModelNameMixin, DeleteView):
	model = System
	template_name = 'deleteview-generic.html'
	success_url = reverse_lazy('results-system-list')


class SystemViewSet(viewsets.ModelViewSet):
	queryset = System.objects.all().order_by('name')
	serializer_class = SystemSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class BucketViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	serializer_class = BucketSerializer
	queryset = Bucket.objects.all()
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class SeriesViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = Series.objects.all().order_by('name')
	serializer_class = SeriesSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class SeriesAttributesViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = SeriesAttributes.objects.all()
	serializer_class = SeriesAttributesSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class SinglePointViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = SinglePoint.objects.all()
	serializer_class = SinglePointSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class SinglePointOuterViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = SinglePointOuter.objects.all()
	serializer_class = SinglePointOuterSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class SinglePointAttributesViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = SinglePointAttributes.objects.all()
	serializer_class = SinglePointAttributesSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class MDRunViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = MDRun.objects.all()
	serializer_class = MDRunSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class MDRunDelete(ModelNameMixin, DeleteView):
	model = MDRun
	template_name = 'deleteview-generic.html'

	def get_success_url(self):
		seriesid = self.object.series_id
		bucketid = self.object.series.bucket_id
		systemid = self.object.series.bucket.system_id
		return reverse('results-series-show', args=[systemid, bucketid, seriesid])


def MDRunHideStop(request, pk):
	try:
		this_run = MDRun.objects.get(pk=pk)
	except:
		raise Http404('System does not exist.')

	try:
		next_run = MDRun.objects.filter(series=this_run.series, part__gt=this_run.part).order_by('part')[:1][0]
	except:
		# this is the last run
		return redirect('results-series-show', system=this_run.series.bucket.system_id, bucket=this_run.series.bucket_id, series=this_run.series_id)

	start_time = next_run.start_time()
	if start_time is None:
		# last run was empty, no overlap
		return redirect('results-series-show', system=this_run.series.bucket.system_id, bucket=this_run.series.bucket_id, series=this_run.series_id)
	this_run.mdstep_set.filter(steptime__gte=start_time).update(masked=True)
	return redirect('results-series-show', system=this_run.series.bucket.system_id, bucket=this_run.series.bucket_id, series=this_run.series_id)


def MDRunHideStart(request, pk):
	try:
		this_run = MDRun.objects.get(pk=pk)
	except:
		raise Http404('System does not exist.')

	try:
		last_run = MDRun.objects.filter(series=this_run.series, part__lt=this_run.part).order_by('-part')[:1][0]
	except:
		# this is the first run
		return redirect('results-series-show', system=this_run.series.bucket.system_id, bucket=this_run.series.bucket_id, series=this_run.series_id)

	stop_time = last_run.stop_time()
	if stop_time is None:
		# last run was empty, no overlap
		return redirect('results-series-show', system=this_run.series.bucket.system_id, bucket=this_run.series.bucket_id, series=this_run.series_id)
	this_run.mdstep_set.filter(steptime__lte=stop_time).update(masked=True)
	return redirect('results-series-show', system=this_run.series.bucket.system_id, bucket=this_run.series.bucket_id, series=this_run.series_id)


def MDRunUnhide(request, pk):
	try:
		this_run = MDRun.objects.get(pk=pk)
	except:
		raise Http404('System does not exist.')

	this_run.mdstep_set.all().update(masked=False)
	return redirect('results-series-show', system=this_run.series.bucket.system_id, bucket=this_run.series.bucket_id, series=this_run.series_id)

class MDStepViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = MDStep.objects.all()
	serializer_class = MDStepSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class AtomViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = Atom.objects.all()
	serializer_class = AtomSerializer
	filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class CoordinateViewSet(LimitUnfilteredQueriesMixin, BulkModelViewSet):
	queryset = Coordinate.objects.all()
	serializer_class = CoordinateSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class CoordinateWrappedViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = CoordinateWrapped.objects.all()
	serializer_class = CoordinateWrappedSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class HirshfeldChargeViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = HirshfeldCharge.objects.all()
	serializer_class = HirshfeldChargeSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class ScaledCoordinateViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = ScaledCoordinate.objects.all()
	serializer_class = ScaledCoordinateSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class ScaledCoordinateWrappedViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = ScaledCoordinateWrapped.objects.all()
	serializer_class = ScaledCoordinateWrappedSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class MullikenChargeViewSet(LimitUnfilteredQueriesMixin, BulkModelViewSet):
	queryset = MullikenCharge.objects.all()
	serializer_class = MullikenChargeSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class MDRunSettingsViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = MDRunSettings.objects.all()
	serializer_class = MDRunSettingsSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class MDRunAttributesViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = MDRunAttributes.objects.all()
	serializer_class = MDRunAttributesSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class StepCellViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = StepCell.objects.all()
	serializer_class = StepCellSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete] + ['mdstep__mdrun', 'mdstep__masked'])


class StepEnsembleViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = StepEnsemble.objects.all()
	serializer_class = StepEnsembleSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete] + ['mdstep__mdrun', 'mdstep__masked'])


class StepContributionsQMViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = StepContributionsQM.objects.all()
	serializer_class = StepContributionsQMSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete] + ['mdstep__mdrun', 'mdstep__masked'])


class StepEnergyViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = StepEnergy.objects.all()
	serializer_class = StepEnergySerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete])


class StepMetaQMViewSet(LimitUnfilteredQueriesMixin, viewsets.ModelViewSet):
	queryset = StepMetaQM.objects.all()
	serializer_class = StepMetaQMSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filter_fields = tuple([_.name for _ in serializer_class.Meta.model._meta.get_fields() if _.concrete] + ['mdstep__mdrun', 'mdstep__masked'])
