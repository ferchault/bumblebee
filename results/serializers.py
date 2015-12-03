from collections import OrderedDict

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


class MullikenChargeSerializer(BulkSerializerMixin, serializers.ModelSerializer):
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


class TransposedListSerializer(serializers.ListSerializer):
	def to_representation(self, data):
		base = super(TransposedListSerializer, self).to_representation(data)

		try:
			request = self.child.context['request']
		except:
			raise ValueError('No request context available.')

		if 'transpose' not in request.query_params:
			return base

		if len(base) == 0:
			return []

		retval = OrderedDict()
		for key in base[0].iterkeys():
			tlist = []
			for item in base:
				tlist.append(item[key])
			retval[key] = tuple(tlist)
		return [retval]


class StepEnsembleSerializer(serializers.ModelSerializer):
	time = serializers.SerializerMethodField('annotate_time')

	class Meta:
		model = StepEnsemble
		fields = tuple([_.name for _ in model._meta.get_fields() if _.concrete] + ['time', ])
		#fields = ('mdstep', 'time', 'temperature', 'pressure')
		list_serializer_class = TransposedListSerializer


	def annotate_time(self, instance):
		try:
			return instance.mdstep.steptime
		except:
			return None

	def to_representation(self, instance):
		base = super(StepEnsembleSerializer, self).to_representation(instance)

		try:
			request = self.context['request']
			selected_fields = request.query_params['fields'].split(',')
			newbase = OrderedDict()
			if len(selected_fields) != 0:
				for key in selected_fields:
					newbase[key] = base[key]
				base = newbase
		except:
			pass
		return base


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
