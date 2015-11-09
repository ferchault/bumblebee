# django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic import ListView, CreateView
from django.core.urlresolvers import reverse_lazy

# app-specific imports
from results.models import *

# rest API imports
from rest_framework import viewsets
from results.serializers import *


def index(request):
	template = loader.get_template('results/index.html')
	systems = System.objects.all()
	context = RequestContext(request, {
		'systems': systems,
	})
	return render(request, 'results/index.html', context)


class SystemListing(ListView):
	model = System
	template_name = 'listview-generic.html'


class SystemCreate(CreateView):
	model = System
	form_class = SystemForm
	success_url = reverse_lazy('results-system-list')
	template_name = 'createview-generic.html'

	def get_context_data(self, **kwargs):
		context = super(SystemCreate, self).get_context_data(**kwargs)
		context['modelname'] = self.model._meta.verbose_name.title()
		return context


class SystemViewSet(viewsets.ModelViewSet):
	queryset = System.objects.all().order_by('name')
	serializer_class = SystemSerializer


class BucketViewSet(viewsets.ModelViewSet):
	queryset = Bucket.objects.all().order_by('name')
	serializer_class = BucketSerializer


class SeriesViewSet(viewsets.ModelViewSet):
	queryset = Series.objects.all().order_by('name')
	serializer_class = SeriesSerializer


class SeriesAttributesViewSet(viewsets.ModelViewSet):
	queryset = SeriesAttributes.objects.all()
	serializer_class = SeriesAttributesSerializer


class SinglePointViewSet(viewsets.ModelViewSet):
	queryset = SinglePoint.objects.all()
	serializer_class = SinglePointSerializer


class SinglePointOuterViewSet(viewsets.ModelViewSet):
	queryset = SinglePointOuter.objects.all()
	serializer_class = SinglePointOuterSerializer


class SinglePointAttributesViewSet(viewsets.ModelViewSet):
	queryset = SinglePointAttributes.objects.all()
	serializer_class = SinglePointAttributesSerializer


class MDRunViewSet(viewsets.ModelViewSet):
	queryset = MDRun.objects.all()
	serializer_class = MDRunSerializer


class MDStepViewSet(viewsets.ModelViewSet):
	queryset = MDStep.objects.all()
	serializer_class = MDStepSerializer


class AtomViewSet(viewsets.ModelViewSet):
	queryset = Atom.objects.all()
	serializer_class = AtomSerializer


class CoordinateViewSet(viewsets.ModelViewSet):
	queryset = Coordinate.objects.all()
	serializer_class = CoordinateSerializer


class CoordinateWrappedViewSet(viewsets.ModelViewSet):
	queryset = CoordinateWrapped.objects.all()
	serializer_class = CoordinateWrappedSerializer


class HirshfeldChargeViewSet(viewsets.ModelViewSet):
	queryset = HirshfeldCharge.objects.all()
	serializer_class = HirshfeldChargeSerializer


class ScaledCoordinateViewSet(viewsets.ModelViewSet):
	queryset = ScaledCoordinate.objects.all()
	serializer_class = ScaledCoordinateSerializer


class ScaledCoordinateWrappedViewSet(viewsets.ModelViewSet):
	queryset = ScaledCoordinateWrapped.objects.all()
	serializer_class = ScaledCoordinateWrappedSerializer


class MullikenChargeViewSet(viewsets.ModelViewSet):
	queryset = MullikenCharge.objects.all()
	serializer_class = MullikenChargeSerializer


class MDRunSettingsViewSet(viewsets.ModelViewSet):
	queryset = MDRunSettings.objects.all()
	serializer_class = MDRunSettingsSerializer


class MDRunAttributesViewSet(viewsets.ModelViewSet):
	queryset = MDRunAttributes.objects.all()
	serializer_class = MDRunAttributesSerializer


class StepCellViewSet(viewsets.ModelViewSet):
	queryset = StepCell.objects.all()
	serializer_class = StepCellSerializer


class StepEnsembleViewSet(viewsets.ModelViewSet):
	queryset = StepEnsemble.objects.all()
	serializer_class = StepEnsembleSerializer


class StepContributionsQMViewSet(viewsets.ModelViewSet):
	queryset = StepContributionsQM.objects.all()
	serializer_class = StepContributionsQMSerializer


class StepEnergyViewSet(viewsets.ModelViewSet):
	queryset = StepEnergy.objects.all()
	serializer_class = StepEnergySerializer


class StepMetaQMViewSet(viewsets.ModelViewSet):
	queryset = StepMetaQM.objects.all()
	serializer_class = StepMetaQMSerializer
