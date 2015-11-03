from django.db import models
from django.forms import ModelForm

class System(models.Model):
	name = models.CharField(max_length=45, help_text="Unique name of the physical system treated in this simulation.")

	@staticmethod
	def explain():
		return ('For each simulation, there is an underlying physical system, i.e. an ethylene dimer, a water box with '
				'120 molecules, a single infinite graphene sheet and so on. For each system, there may be a number of '
				'representations in terms of different topologies and atom kinds. A system definition is used for '
				'grouping similar simulations.')

class SystemForm(ModelForm):
	class Meta:
		model = System
		fields = '__all__'

class Bucket(models.Model):
	name = models.CharField(max_length=45)
	token = models.CharField(max_length=50)
	comment = models.CharField(max_length=200)
	updated = models.DateTimeField()
	system = models.ForeignKey(System)

class Series(models.Model):
	name = models.CharField(max_length=45)
	bucket = models.ForeignKey(Bucket)

class SeriesAttributes(models.Model):
	key = models.CharField(max_length=45)
	value = models.CharField(max_length=100)
	series = models.ForeignKey(Series)

class SinglePoint(models.Model):
	name = models.CharField(max_length=45)
	series = models.ForeignKey(Series)

class SinglePointOuter(models.Model):
	lagrangian = models.FloatField()
	orderparameter = models.FloatField()
	gradient = models.FloatField()
	scfcycles = models.IntegerField()
	otnumber = models.IntegerField()

class SinglePointAttributes(models.Model):
	key = models.CharField(max_length=45)
	value = models.CharField(max_length=100)
	series = models.ForeignKey(Series)