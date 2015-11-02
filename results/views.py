# django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

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
	return HttpResponse(template.render(context))

class SystemViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows Systems to be viewed or edited.
	"""
	queryset = System.objects.all().order_by('name')
	serializer_class = SystemSerializer