from django.db import models

# Create your models here.

class Address(models.Model):
	user_input = models.CharField(max_length=1000)
	creation_time = models.DateTimeField('date created')	
