from results.models import *
from rest_framework import serializers
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)


class SystemSerializer(serializers.ModelSerializer):
	class Meta:
		model = System
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class BucketSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bucket
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class SeriesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Series
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class SeriesAttributesSerializer(serializers.ModelSerializer):
	class Meta:
		model = SeriesAttributes
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class SinglePointSerializer(serializers.ModelSerializer):
	class Meta:
		model = SinglePoint
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class SinglePointOuterSerializer(serializers.ModelSerializer):
	class Meta:
		model = SinglePointOuter
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class SinglePointAttributesSerializer(serializers.ModelSerializer):
	class Meta:
		model = SinglePointAttributes
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class MDRunSerializer(serializers.ModelSerializer):
	class Meta:
		model = MDRun
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class MDStepSerializer(serializers.ModelSerializer):
	class Meta:
		model = MDStep
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class AtomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Atom
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class CoordinateSerializer(BulkSerializerMixin, serializers.ModelSerializer):
	class Meta:
		model = Coordinate
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class CoordinateWrappedSerializer(serializers.ModelSerializer):
	class Meta:
		model = CoordinateWrapped
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class HirshfeldChargeSerializer(serializers.ModelSerializer):
	class Meta:
		model = HirshfeldCharge
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class ScaledCoordinateSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScaledCoordinate
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class ScaledCoordinateWrappedSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScaledCoordinateWrapped
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class MullikenChargeSerializer(serializers.ModelSerializer):
	class Meta:
		model = MullikenCharge
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class MDRunSettingsSerializer(serializers.ModelSerializer):
	class Meta:
		model = MDRunSettings
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class MDRunAttributesSerializer(serializers.ModelSerializer):
	class Meta:
		model = MDRunAttributes
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class StepCellSerializer(serializers.ModelSerializer):
	class Meta:
		model = StepCell
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class StepEnsembleSerializer(serializers.ModelSerializer):
	class Meta:
		model = StepEnsemble
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class StepContributionsQMSerializer(serializers.ModelSerializer):
	class Meta:
		model = StepContributionsQM
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class StepEnergySerializer(serializers.ModelSerializer):
	class Meta:
		model = StepEnergy
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])


class StepMetaQMSerializer(serializers.ModelSerializer):
	class Meta:
		model = StepMetaQM
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete])
