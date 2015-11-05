# django modules
from django.db import models
from django.forms import ModelForm

# app-specific imports
from bumblebee.models import ExplainableMixin


class Project(models.Model, ExplainableMixin):
	name = models.CharField(max_length=45, verbose_name="Project Name", help_text="The name this project is referred to.")
	active = models.BooleanField()

	def detailed(self):
		return '%s %s' % (self._meta.verbose_name, self.name)


class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = '__all__'


class TodoStatus(models.Model, ExplainableMixin):
	name = models.CharField(max_length=30)
	completed = models.BooleanField()


class TodoStatusForm(ModelForm):
	class Meta:
		model = TodoStatus
		fields = '__all__'


class TodoPriority(models.Model, ExplainableMixin):
	name = models.CharField(max_length=20)
	priority = models.IntegerField()


class TodoPriorityForm(ModelForm):
	class Meta:
		model = TodoPriority
		fields = '__all__'


class TodoEntry(models.Model, ExplainableMixin):
	task = models.CharField(max_length=200)
	project = models.ForeignKey(Project)
	duedate = models.DateField()
	priority = models.ForeignKey(TodoPriority)
	status = models.ForeignKey(TodoStatus)


class TodoEntryForm(ModelForm):
	class Meta:
		model = TodoEntry
		fields = '__all__'
