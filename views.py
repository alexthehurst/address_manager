from django.shortcuts import render
from django.views import generic
from .models import Address

from .forms import BulkImportForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.

class AllAddressesView(generic.ListView):
	template_name = 'addman/all_addresses.html'
	context_object_name = 'all_addresses_list'
	def get_queryset(self):
		"""Return all the addresses in the database."""
		return Address.objects.all()

def bulk_import_view(request):
	if request.method=='POST':
		form = BulkImportForm(request.POST)
		form_is_valid = form.is_valid() #Side effect is to create the cleaned_data
		user_lines = form.cleaned_data['bulk_addresses'].strip().split('\n')
		if not form_is_valid:
			error_msg = "The form submitted was invalid."
		elif not len(user_lines) <= 500:
			error_msg = "Sorry, bulk imports are limited to 500 rows per round."
		else:
			for line in user_lines:
				Address.objects.create(user_input=line)
			notice = "Thanks for the submission. Those addresses have been imported."
			return HttpResponseRedirect(reverse('addman:all_addresses'), )
		return render(request, 'addman/bulk_import.html', context={'form': form, 'error_msg': error_msg,})
	
	else:
		form = BulkImportForm()
		return render(request, 'addman/bulk_import.html', context={'form': form,} )
