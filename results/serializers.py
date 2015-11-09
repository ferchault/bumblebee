from results.models import *
from rest_framework import serializers


class SystemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = System
		fields = ('name',)


class BucketSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Bucket
		fields = ('name', 'token', 'comment', 'updated', 'system')


class SeriesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Series
		fields = ('name', 'bucket')


class SeriesAttributesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = SeriesAttributes
		fields = ('key', 'value', 'series')


class SinglePointSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = SinglePoint
		fields = ('name', 'series')


class SinglePointOuterSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = SinglePointOuter
		fields = ('lagrangian', 'orderparameter', 'gradient', 'scfcycles', 'otnumber')


class SinglePointAttributesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = SinglePointAttributes
		fields = ('key', 'value', 'series')


class MDRunSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = MDRun
		fields = ('part', 'type', 'series')


class MDStepSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = MDStep
		fields = ('mdrun', 'stepnumber', 'steptime', 'masked')


class AtomSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Atom
		fields = ('element', 'kind', 'system')


class CoordinateSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Coordinate
		fields = ('x', 'y', 'z', 'atom', 'mdstep')


class CoordinateWrappedSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = CoordinateWrapped
		fields = ('x', 'y', 'z', 'coordinate')


class HirshfeldChargeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = HirshfeldCharge
		fields = ('charge', 'alpha', 'beta', 'spin', 'reference', 'atom', 'mdstep')


class ScaledCoordinateSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ScaledCoordinate
		fields = ('x', 'y', 'z', 'atom', 'mdstep')


class ScaledCoordinateWrappedSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ScaledCoordinateWrapped
		fields = ('x', 'y', 'z', 'scaledcoordinate')


class MullikenChargeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = MullikenCharge
		fields = ('charge', 'alpha', 'beta', 'spin', 'atom', 'mdstep')


class MDRunSettingsSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = MDRunSettings
		fields = ('temperature', 'pressure', 'multiplicity', 'timestep', 'mdrun')


class MDRunAttributesSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = MDRunAttributes
		fields = ('key', 'value', 'mdrun')


class StepCellSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = StepCell
		fields = ('a', 'b', 'c', 'alpha', 'beta', 'gamma', 'mdstep')


class StepEnsembleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = StepEnsemble
		fields = ('temperature', 'pressure', 'volume', 'conserved', 'mdstep')


class StepContributionsQMSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = StepContributionsQM
		fields = ('coreselfenergy', 'corehamiltonian', 'hartree', 'xc', 'hfx', 'dispersion', 'constraint', 'mdstep')


class StepEnergySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = StepEnergy
		fields = ('etot', 'epot', 'ekin', 'drift', 'mdstep')


class StepMetaQMSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = StepMetaQM
		fields = ('iasd', 's2', 'scfcycles', 'otcycles', 'mdstep')
