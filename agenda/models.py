# django modules
from django.db import models
from django.forms import ModelForm
from django.utils.deconstruct import deconstructible
from django.apps import apps
from django.core.exceptions import ValidationError

# app-specific imports
from bumblebee.models import ExplainableMixin


@deconstructible
class LimitSelfReferenceDepth(object):
	def __init__(self, maxdepth, model):
		self._maxdepth = maxdepth
		self._model = model

	def __call__(self, value):
		if value is None:
			return
		model = apps.get_model(app_label='agenda', model_name=self._model)
		depth = 1
		while True:
			parent = model.objects.get(pk=value).parent
			if parent is None:
				break
			else:
				value = parent.id
				depth += 1
				if depth > self._maxdepth:
					raise ValidationError('No nesting for more than %d levels allowed.' % self._maxdepth)


class Project(models.Model, ExplainableMixin):
	name = models.CharField(max_length=45, verbose_name="Project Name", help_text="The name this project is referred to.")
	active = models.BooleanField(verbose_name='Active?')
	parent = models.ForeignKey('self', validators=[LimitSelfReferenceDepth(1, 'Project')], default=None, null=True)

	def detailed(self):
		return '%s %s' % (self._meta.verbose_name, self.name)

	def __unicode__(self):
		return self.name


class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = '__all__'


class TodoStatus(models.Model, ExplainableMixin):
	name = models.CharField(max_length=30)
	completed = models.BooleanField()

	def __unicode__(self):
		return self.name


class TodoStatusForm(ModelForm):
	class Meta:
		model = TodoStatus
		fields = '__all__'


class TodoPriority(models.Model, ExplainableMixin):
	name = models.CharField(max_length=20)
	priority = models.IntegerField()

	def __unicode__(self):
		return self.name


class TodoPriorityForm(ModelForm):
	class Meta:
		model = TodoPriority
		fields = '__all__'


class TodoEntry(models.Model, ExplainableMixin):
	task = models.CharField(max_length=200)
	project = models.ForeignKey(Project)
	duedate = models.DateField(null=True, blank=True)
	priority = models.ForeignKey(TodoPriority)
	status = models.ForeignKey(TodoStatus)


class TodoEntryForm(ModelForm):
	class Meta:
		model = TodoEntry
		fields = '__all__'
