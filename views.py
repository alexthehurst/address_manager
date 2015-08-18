from django.shortcuts import render
from django.views import generic
from .models import Address

# Create your views here.

class AllAddressesView(generic.ListView):
	template_name = 'addman/all_addresses.html'
	context_object_name = 'all_addresses_list'
	def get_queryset(self):
		"""Return all the addresses in the database."""
		return Address.objects.all()
