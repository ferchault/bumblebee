# django modules
from django.db import models
from rest_framework import metadata,serializers

class ExplainableMixin(object):
	def get_fields(self):
		return [field for field in self._meta.fields]

	def get_field_values(self):
		return [field.value_to_string(self) for field in self._meta.fields]

	def detailed(self):
		return self._meta.verbose_name

	@staticmethod
	def explain():
		return ('No explanation available.')

class ModelNameMixin(object):
	def get_context_data(self, **kwargs):
		context = super(ModelNameMixin, self).get_context_data(**kwargs)
		context['modelname'] = self.model._meta.verbose_name.title()
		try:
			fields = self.fields

			context['fields'] = fields
		except:
			context['fields'] = [_.name for _ in self.model._meta.fields]
		return context

class CondensedMetadata(metadata.SimpleMetadata):
	"""
	Don't include related field choices for `OPTIONS` requests.
	"""
	def get_field_info(self, field):
		base = super(CondensedMetadata, self).get_field_info(field)
		if type(field) == serializers.PrimaryKeyRelatedField:
			base['choices'] = 'Related field choices not listed.'
		return base