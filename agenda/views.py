from django.shortcuts import render

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

# app-specific imports
from agenda.models import *
from bumblebee.models import ModelNameMixin

class ProjectListing(ModelNameMixin, ListView):
	model = Project
	template_name = 'listview-generic.html'

class ProjectCreate(ModelNameMixin, CreateView):
	model = Project
	form_class = ProjectForm
	success_url = reverse_lazy('agenda-project-list')
	template_name = 'createview-generic.html'

class ProjectUpdate(ModelNameMixin, UpdateView):
	model = Project
	fields = ['name', 'active']
	template_name = 'updateview-generic.html'
	success_url = reverse_lazy('agenda-project-list')

class ProjectDelete(ModelNameMixin, DeleteView):
	model = Project
	success_url = reverse_lazy('agenda-project-list')
	template_name = 'deleteview-generic.html'