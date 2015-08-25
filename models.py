from django.db import models
from django.utils import timezone

# Create your models here.

class AddressSet(models.Model):
	set_name = models.CharField(max_length=150)
	set_description = models.CharField(max_length=1000, blank=True)
	creation_time = models.DateTimeField('date created', default=timezone.now)
	update_time = models.DateTimeField('date created', default=timezone.now)
	owner = models.CharField(max_length=30)
	def __str__(self):
		return(self.set_name)

class Address(models.Model):
	user_input = models.CharField(max_length=1000)
	creation_time = models.DateTimeField('date created', default=timezone.now)
	address_set = models.ForeignKey(AddressSet)
	def __str__(self):
		return(self.user_input)

