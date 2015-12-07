# django modules
from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from bumblebee.models import ExplainableMixin


class System(models.Model, ExplainableMixin):
	name = models.CharField(max_length=45, verbose_name='test', help_text="Unique name of the physical system treated in this simulation.")

	@staticmethod
	def explain():
		return ('For each simulation, there is an underlying physical system, i.e. an ethylene dimer, a water box with '
				'120 molecules, a single infinite graphene sheet and so on. For each system, there may be a number of '
				'representations in terms of different topologies and atom kinds. A system definition is used for '
				'grouping similar simulations.')

	alias = {'bucket_count': 'Bucket count', 'name': 'System'}
	link = 'name'

	def __str__(self):
		return self.name


class SystemForm(ModelForm):
	class Meta:
		model = System
		fields = '__all__'


class Bucket(models.Model, ExplainableMixin):
	name = models.CharField(max_length=45)
	token = models.CharField(max_length=50, blank=True)
	comment = models.CharField(max_length=200, blank=True)
	updated = models.DateTimeField(blank=True)
	system = models.ForeignKey(System)

	def save(self, *args, **kwargs):
		if not self.id:
			self.updated = timezone.now()
		return super(Bucket, self).save(*args, **kwargs)

	link = 'name'
	alias = {'name': 'Bucket'}

	def __str__(self):
		return self.name


class Series(models.Model, ExplainableMixin):
	name = models.CharField(max_length=45)
	bucket = models.ForeignKey(Bucket)

	link = 'name'
	alias = {'name': 'Series'}

	def __str__(self):
		return self.name

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
	type = models.CharField(max_length=20, blank=True)
	series = models.ForeignKey(Series)

	def start_time(self):
		mdsteps =  self.mdstep_set.filter(masked=False).order_by('steptime')[:1]
		if len(mdsteps) == 0:
			return None
		else:
			return mdsteps[0].steptime

	def stop_time(self):
		mdsteps =  self.mdstep_set.filter(masked=False).order_by('-steptime')[:1]
		if len(mdsteps) == 0:
			return None
		else:
			return mdsteps[0].steptime

	def duration(self):
		try:
			return self.stop_time()-self.start_time()
		except:
			return None

	def overlap_before(self):
		return 0

	def overlap_after(self):
		return 0

	def detailed(self):
		return '%s.%s.%s.%d' % (self.series.bucket.system, self.series.bucket, self.series, self.part)


class MDStep(models.Model, ExplainableMixin):
	mdrun = models.ForeignKey(MDRun)
	stepnumber = models.IntegerField(blank=True, null=True)
	steptime = models.FloatField(blank=True, null=True)
	masked = models.NullBooleanField(blank=True, default=False)


class Atom(models.Model, ExplainableMixin):
	element = models.CharField(max_length=3, blank=True, null=True)
	kind = models.CharField(max_length=10)
	number = models.IntegerField(default=0)
	system = models.ForeignKey(System)


class Coordinate(models.Model, ExplainableMixin):
	x = models.FloatField(blank=True, null=True)
	y = models.FloatField(blank=True, null=True)
	z = models.FloatField(blank=True, null=True)
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
	charge = models.FloatField(blank=True, null=True)
	alpha = models.FloatField(blank=True, null=True)
	beta = models.FloatField(blank=True, null=True)
	spin = models.FloatField(blank=True, null=True)
	atom = models.ForeignKey(Atom)
	mdstep = models.ForeignKey(MDStep)


class MDRunSettings(models.Model, ExplainableMixin):
	temperature = models.FloatField(blank=True, null=True)
	pressure = models.FloatField(blank=True, null=True)
	multiplicity = models.IntegerField(blank=True, null=True)
	timestep = models.FloatField(blank=True, null=True)
	mdrun = models.ForeignKey(MDRun)


class MDRunAttributes(models.Model, ExplainableMixin):
	key = models.CharField(max_length=45)
	value = models.CharField(max_length=200)
	mdrun = models.ForeignKey(MDRun)


class StepCell(models.Model, ExplainableMixin):
	a = models.FloatField(blank=True, null=True)
	b = models.FloatField(blank=True, null=True)
	c = models.FloatField(blank=True, null=True)
	alpha = models.FloatField(blank=True, null=True)
	beta = models.FloatField(blank=True, null=True)
	gamma = models.FloatField(blank=True, null=True)
	mdstep = models.ForeignKey(MDStep)


class StepEnsemble(models.Model, ExplainableMixin):
	temperature = models.FloatField(blank=True, null=True)
	pressure = models.FloatField(blank=True, null=True)
	volume = models.FloatField(blank=True, null=True)
	conserved = models.FloatField(blank=True, null=True)
	mdstep = models.ForeignKey(MDStep)


class StepContributionsQM(models.Model, ExplainableMixin):
	coreselfenergy = models.FloatField(blank=True, null=True)
	corehamiltonian = models.FloatField(blank=True, null=True)
	hartree = models.FloatField(blank=True, null=True)
	xc = models.FloatField(blank=True, null=True)
	hfx = models.FloatField(blank=True, null=True)
	dispersion = models.FloatField(blank=True, null=True)
	constraint = models.FloatField(blank=True, null=True)
	mdstep = models.ForeignKey(MDStep)


class StepEnergy(models.Model, ExplainableMixin):
	etot = models.FloatField(blank=True, null=True)
	epot = models.FloatField(blank=True, null=True)
	ekin = models.FloatField(blank=True, null=True)
	drift = models.FloatField(blank=True, null=True)
	mdstep = models.ForeignKey(MDStep)


class StepMetaQM(models.Model, ExplainableMixin):
	iasd = models.FloatField(blank=True, null=True)
	s2 = models.FloatField(blank=True, null=True)
	scfcycles = models.FloatField(blank=True, null=True)
	otcycles = models.FloatField(blank=True, null=True)
	mdstep = models.ForeignKey(MDStep)
