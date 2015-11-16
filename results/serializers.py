from results.models import *
from rest_framework import serializers


class SystemSerializer(serializers.ModelSerializer):
	class Meta:
		model = System
		fields = ('id', 'name',)


class BucketSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bucket
		fields = ('id', 'name', 'token', 'comment', 'updated', 'system')


class SeriesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Series
		fields = ('id', 'name', 'bucket')


class SeriesAttributesSerializer(serializers.ModelSerializer):
	class Meta:
		model = SeriesAttributes
		fields = ('key', 'value', 'series')


class SinglePointSerializer(serializers.ModelSerializer):
	class Meta:
		model = SinglePoint
		fields = ('name', 'series')


class SinglePointOuterSerializer(serializers.ModelSerializer):
	class Meta:
		model = SinglePointOuter
		fields = ('lagrangian', 'orderparameter', 'gradient', 'scfcycles', 'otnumber')


class SinglePointAttributesSerializer(serializers.ModelSerializer):
	class Meta:
		model = SinglePointAttributes
		fields = ('key', 'value', 'series')


class MDRunSerializer(serializers.ModelSerializer):
	class Meta:
		model = MDRun
		fields = ('part', 'type', 'series')


class MDStepSerializer(serializers.ModelSerializer):
	class Meta:
		model = MDStep
		fields = ('mdrun', 'stepnumber', 'steptime', 'masked')


class AtomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Atom
		fields = ('element', 'kind', 'system')


class CoordinateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Coordinate
		fields = ('x', 'y', 'z', 'atom', 'mdstep')


class CoordinateWrappedSerializer(serializers.ModelSerializer):
	class Meta:
		model = CoordinateWrapped
		fields = ('x', 'y', 'z', 'coordinate')


class HirshfeldChargeSerializer(serializers.ModelSerializer):
	class Meta:
		model = HirshfeldCharge
		fields = ('charge', 'alpha', 'beta', 'spin', 'reference', 'atom', 'mdstep')


class ScaledCoordinateSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScaledCoordinate
		fields = ('x', 'y', 'z', 'atom', 'mdstep')


class ScaledCoordinateWrappedSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScaledCoordinateWrapped
		fields = ('x', 'y', 'z', 'scaledcoordinate')


class MullikenChargeSerializer(serializers.ModelSerializer):
	class Meta:
		model = MullikenCharge
		fields = ('charge', 'alpha', 'beta', 'spin', 'atom', 'mdstep')


class MDRunSettingsSerializer(serializers.ModelSerializer):
	class Meta:
		model = MDRunSettings
		fields = ('temperature', 'pressure', 'multiplicity', 'timestep', 'mdrun')


class MDRunAttributesSerializer(serializers.ModelSerializer):
	class Meta:
		model = MDRunAttributes
		fields = ('key', 'value', 'mdrun')


class StepCellSerializer(serializers.ModelSerializer):
	class Meta:
		model = StepCell
		fields = ('a', 'b', 'c', 'alpha', 'beta', 'gamma', 'mdstep')


class StepEnsembleSerializer(serializers.ModelSerializer):
	class Meta:
		model = StepEnsemble
		fields = ('temperature', 'pressure', 'volume', 'conserved', 'mdstep')


class StepContributionsQMSerializer(serializers.ModelSerializer):
	class Meta:
		model = StepContributionsQM
		fields = ('coreselfenergy', 'corehamiltonian', 'hartree', 'xc', 'hfx', 'dispersion', 'constraint', 'mdstep')


class StepEnergySerializer(serializers.ModelSerializer):
	class Meta:
		model = StepEnergy
		fields = ('etot', 'epot', 'ekin', 'drift', 'mdstep')


class StepMetaQMSerializer(serializers.ModelSerializer):
	class Meta:
		model = StepMetaQM
		fields = ('iasd', 's2', 'scfcycles', 'otcycles', 'mdstep')
