from django.db import models

class System(models.Model):
	name = models.CharField(max_length=45)

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