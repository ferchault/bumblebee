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
	"""
	API endpoint that allows Systems to be viewed or edited.
	"""
	queryset = System.objects.all().order_by('name')
	serializer_class = SystemSerializer