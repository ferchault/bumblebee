# django imports
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext, loader
from django.shortcuts import render

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


class StatusListing(ModelNameMixin, ListView):
	model = TodoStatus
	template_name = 'listview-generic.html'


class StatusCreate(ModelNameMixin, CreateView):
	model = TodoStatus
	form_class = TodoStatusForm
	success_url = reverse_lazy('agenda-status-list')
	template_name = 'createview-generic.html'


class StatusUpdate(ModelNameMixin, UpdateView):
	model = TodoStatus
	fields = ['name', 'waitingexternal', 'needshuman', 'completed']
	template_name = 'updateview-generic.html'
	success_url = reverse_lazy('agenda-status-list')


class StatusDelete(ModelNameMixin, DeleteView):
	model = TodoStatus
	success_url = reverse_lazy('agenda-status-list')
	template_name = 'deleteview-generic.html'


class PriorityListing(ModelNameMixin, ListView):
	model = TodoPriority
	template_name = 'listview-generic.html'


class PriorityCreate(ModelNameMixin, CreateView):
	model = TodoPriority
	form_class = TodoPriorityForm
	success_url = reverse_lazy('agenda-priority-list')
	template_name = 'createview-generic.html'


class PriorityUpdate(ModelNameMixin, UpdateView):
	model = TodoPriority
	fields = '__all__'
	template_name = 'updateview-generic.html'
	success_url = reverse_lazy('agenda-priority-list')


class PriorityDelete(ModelNameMixin, DeleteView):
	model = TodoPriority
	success_url = reverse_lazy('agenda-priority-list')
	template_name = 'deleteview-generic.html'


class EntryListing(ModelNameMixin, ListView):
	model = TodoEntry
	template_name = 'listview-generic.html'


class EntryCreate(ModelNameMixin, CreateView):
	model = TodoEntry
	form_class = TodoEntryForm
	success_url = reverse_lazy('agenda-entry-list')
	template_name = 'createview-generic.html'


class EntryUpdate(ModelNameMixin, UpdateView):
	model = TodoEntry
	fields = ['task', 'project', 'duedate', 'priority', 'status']
	template_name = 'updateview-generic.html'
	success_url = reverse_lazy('agenda-entry-list')


class EntryDelete(ModelNameMixin, DeleteView):
	model = TodoEntry
	success_url = reverse_lazy('agenda-entry-list')
	template_name = 'deleteview-generic.html'


def overview(request):
	human_actions = TodoEntry.objects.filter(status__needshuman = True)
	waiting_actions = TodoEntry.objects.filter(status__waitingexternal = True)
	other_actions = TodoEntry.objects.filter(status__needshuman = False, status__waitingexternal=False)
	context = RequestContext(request, {
		'human': human_actions,
		'waiting': waiting_actions,
		'other': other_actions
	})
	return render(request, 'agenda/overview.html', context)