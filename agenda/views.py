from django.shortcuts import render

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

# app-specific imports
from agenda.models import *

class ProjectListing(ListView):
	model = Project
	template_name = 'listview-generic.html'

	def get_context_data(self, **kwargs):
		context = super(ProjectListing, self).get_context_data(**kwargs)
		context['modelname'] = self.model._meta.verbose_name.title()
		return context

class ProjectCreate(CreateView):
	model = Project
	form_class = ProjectForm
	success_url = reverse_lazy('agenda-project-list')
	template_name = 'createview-generic.html'

	def get_context_data(self, **kwargs):
		context = super(ProjectCreate, self).get_context_data(**kwargs)
		context['modelname'] = self.model._meta.verbose_name.title()
		return context

class ProjectUpdate(UpdateView):
	model = Project
	fields = ['name', 'active']
	template_name = 'updateview-generic.html'
	success_url = reverse_lazy('agenda-project-list')

	def get_context_data(self, **kwargs):
		context = super(ProjectUpdate, self).get_context_data(**kwargs)
		context['modelname'] = self.model._meta.verbose_name.title()
		return context

class ProjectDelete(DeleteView):
	model = Project
	success_url = reverse_lazy('agenda-project-list')
	template_name = 'deleteview-generic.html'

	def get_context_data(self, **kwargs):
		context = super(ProjectDelete, self).get_context_data(**kwargs)
		context['modelname'] = self.model._meta.verbose_name.title()
		return context