# django modules
from django.db import models

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
		return context