from results.models import System
from rest_framework import serializers

class SystemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = System
		fields = ('name',)