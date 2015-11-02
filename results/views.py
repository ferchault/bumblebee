from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from results.models import *

def index(request):
	template = loader.get_template('results/index.html')
	systems = System.objects.all()
	context = RequestContext(request, {
		'systems': systems,
	})
	return HttpResponse(template.render(context))
