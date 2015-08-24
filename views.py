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
		# error_msg = None
		#if not(form.is_valid()):
	#		error_msg = "The form submitted was invalid."
			# Here we want to return to the bulk_import form with an error_msg.
		#elif 'bulk_addresses' not in form.cleaned_data:
		#	error_msg = 'Please supply one or more addresses.'
		if not form.is_valid():
			return render(request, 'addman/bulk_import.html', context={'form': form, })
		#else:	
		# try:
		# 	user_lines = form.cleaned_data['bulk_addresses'].strip().split('\n')
		# except KeyError:
		# 	error_msg = "Please try again with some input in the form."
		# if len(user_lines) > 500:
		# 	error_msg = "Sorry, bulk imports are limited to 500 rows per round."
		else:
			try:
				for line in user_lines:
					Address.objects.create(user_input=line)
			except:
				notice = "There was an error importing addresses. The import was stopped at '%s'." % line
				return render(request, 'addman/bulk_import.html', context={'form': form, })
			notice = "Thanks for the submission. Those addresses have been imported."
			return HttpResponseRedirect(reverse('addman:all_addresses'), )
	
	else: # GET
		form = BulkImportForm()
		return render(request, 'addman/bulk_import.html', context={'form': form,} )
