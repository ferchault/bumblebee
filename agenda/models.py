# django imports
from django.db import models

# project-specific imports
from bumblebee.models import Explainable

class Project(models.Model, Explainable):
	name = models.CharField(max_length=45)
	active = models.BooleanField()

class TodoStatus(models.Model, Explainable):
	name = models.CharField(max_length=30)
	completed = models.BooleanField()

class TodoPriority(models.Model, Explainable):
	name = models.CharField(max_length=20)
	priority = models.IntegerField()

class TodoEntry(models.Model, Explainable):
	task = models.CharField(max_length=200)
	project = models.ForeignKey(Project)
	duedate = models.DateField()
	priority = models.ForeignKey(TodoPriority)
	status = models.ForeignKey(TodoStatus)