# django modules
from django.db import models
from django.forms import ModelForm
from bumblebee.models import ExplainableMixin


class System(models.Model, ExplainableMixin):
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


class Bucket(models.Model, ExplainableMixin):
	name = models.CharField(max_length=45)
	token = models.CharField(max_length=50)
	comment = models.CharField(max_length=200)
	updated = models.DateTimeField()
	system = models.ForeignKey(System)


class Series(models.Model, ExplainableMixin):
	name = models.CharField(max_length=45)
	bucket = models.ForeignKey(Bucket)


class SeriesAttributes(models.Model, ExplainableMixin):
	key = models.CharField(max_length=45)
	value = models.CharField(max_length=100)
	series = models.ForeignKey(Series)


class SinglePoint(models.Model, ExplainableMixin):
	name = models.CharField(max_length=45)
	series = models.ForeignKey(Series)


class SinglePointOuter(models.Model, ExplainableMixin):
	lagrangian = models.FloatField()
	orderparameter = models.FloatField()
	gradient = models.FloatField()
	scfcycles = models.IntegerField()
	otnumber = models.IntegerField()


class SinglePointAttributes(models.Model, ExplainableMixin):
	key = models.CharField(max_length=45)
	value = models.CharField(max_length=100)
	series = models.ForeignKey(Series)


class MDRun(models.Model, ExplainableMixin):
	part = models.IntegerField()
	type = models.CharField(max_length=20)
	series = models.ForeignKey(Series)


class MDStep(models.Model, ExplainableMixin):
	mdrun = models.ForeignKey(MDRun)
	stepnumber = models.IntegerField()
	steptime = models.FloatField()
	masked = models.BooleanField()


class Atom(models.Model, ExplainableMixin):
	element = models.CharField(max_length=3)
	kind = models.CharField(max_length=10)
	system = models.ForeignKey(System)


class Coordinate(models.Model, ExplainableMixin):
	x = models.FloatField()
	y = models.FloatField()
	z = models.FloatField()
	atom = models.ForeignKey(Atom)
	mdstep = models.ForeignKey(MDStep)


class CoordinateWrapped(models.Model, ExplainableMixin):
	x = models.FloatField()
	y = models.FloatField()
	z = models.FloatField()
	coordinate = models.ForeignKey(Coordinate)


class HirshfeldCharge(models.Model, ExplainableMixin):
	charge = models.FloatField()
	alpha = models.FloatField()
	beta = models.FloatField()
	spin = models.FloatField()
	reference = models.FloatField()
	atom = models.ForeignKey(Atom)
	mdstep = models.ForeignKey(MDStep)


class ScaledCoordinate(models.Model, ExplainableMixin):
	x = models.FloatField()
	y = models.FloatField()
	z = models.FloatField()
	atom = models.ForeignKey(Atom)
	mdstep = models.ForeignKey(MDStep)


class ScaledCoordinateWrapped(models.Model, ExplainableMixin):
	x = models.FloatField()
	y = models.FloatField()
	z = models.FloatField()
	scaledcoordinate = models.ForeignKey(ScaledCoordinate)


class MullikenCharge(models.Model, ExplainableMixin):
	charge = models.FloatField()
	alpha = models.FloatField()
	beta = models.FloatField()
	spin = models.FloatField()
	atom = models.ForeignKey(Atom)
	mdstep = models.ForeignKey(MDStep)


class MDRunSettings(models.Model, ExplainableMixin):
	temperature = models.FloatField()
	pressure = models.FloatField()
	multiplicity = models.IntegerField()
	timestep = models.FloatField()
	mdrun = models.ForeignKey(MDRun)


class MDRunAttributes(models.Model, ExplainableMixin):
	key = models.CharField(max_length=45)
	value = models.CharField(max_length=200)
	mdrun = models.ForeignKey(MDRun)


class StepCell(models.Model, ExplainableMixin):
	a = models.FloatField()
	b = models.FloatField()
	c = models.FloatField()
	alpha = models.FloatField()
	beta = models.FloatField()
	gamma = models.FloatField()
	mdstep = models.ForeignKey(MDStep)


class StepEnsemble(models.Model, ExplainableMixin):
	temperature = models.FloatField()
	pressure = models.FloatField()
	volume = models.FloatField()
	conserved = models.FloatField()
	mdstep = models.ForeignKey(MDStep)


class StepContributionsQM(models.Model, ExplainableMixin):
	coreselfenergy = models.FloatField()
	corehamiltonian = models.FloatField()
	hartree = models.FloatField()
	xc = models.FloatField()
	hfx = models.FloatField()
	dispersion = models.FloatField()
	constraint = models.FloatField()
	mdstep = models.ForeignKey(MDStep)


class StepEnergy(models.Model, ExplainableMixin):
	etot = models.FloatField()
	epot = models.FloatField()
	ekin = models.FloatField()
	drift = models.FloatField()
	mdstep = models.ForeignKey(MDStep)


class StepMetaQM(models.Model, ExplainableMixin):
	iasd = models.FloatField()
	s2 = models.FloatField()
	scfcycles = models.FloatField()
	otcycles = models.FloatField()
	mdstep = models.ForeignKey(MDStep)
