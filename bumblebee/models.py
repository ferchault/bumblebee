# django modules
from django.db import models

class Explainable(object):
	def get_fields(self):
		return [field for field in self._meta.fields]

	def get_field_values(self):
		return [field.value_to_string(self) for field in self._meta.fields]

	@staticmethod
	def explain():
		return ('No explanation available.')
