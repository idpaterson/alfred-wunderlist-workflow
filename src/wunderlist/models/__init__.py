from peewee import DateTimeField
from datetime import datetime
from dateutil.tz import tzutc
from wunderlist.util import utc_to_local

class DateTimeUTCField(DateTimeField):
	def python_value(self, value):
		value = super(DateTimeUTCField, self).python_value(value)

		if isinstance(value, datetime):
			value = value.replace(tzinfo=tzutc())
		return value

	def db_value(self, value):
		if isinstance(value, datetime):
			value = value.replace(tzinfo=None)

		return super(DateTimeUTCField, self).db_value(value)

	def _get_local_datetime_descriptor(self):
		return LocalDateTimeDescriptor(self)

	def add_to_class(self, model_class, name):
		"""Add a corresponding property with the local datetime"""
		super(DateTimeUTCField, self).add_to_class(model_class, name)

		setattr(model_class, name + '_local', self._get_local_datetime_descriptor())

class LocalDateTimeDescriptor(object):
	"""Gives direct access to the localized datetime"""
	def __init__(self, field):
		self.attr_name = field.name

	def __get__(self, instance, instance_type=None):
		if instance is not None:
			dt = instance._data.get(self.attr_name)

			return utc_to_local(dt)
