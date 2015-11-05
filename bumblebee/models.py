# django modules
from django.db import models

class Explainable(object):
	def get_fields(self):
		return [field for field in self._meta.fields]

	def get_field_values(self):
		return [field.value_to_string(self) for field in self._meta.fields]

	def detailed(self):
		return self._meta.verbose_name

	@staticmethod
	def explain():
		return ('No explanation available.')
