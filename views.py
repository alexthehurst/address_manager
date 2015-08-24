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
		if not form.is_valid():
			return render(request, 'addman/bulk_import.html', context={'form': form, })
		else:
		 	user_lines = form.cleaned_data['bulk_addresses'].strip().split('\n')
			for line in user_lines:
				try:
					Address.objects.create(user_input=line)
				except:
					notice = "There was an error importing addresses. The import was stopped at '%s'." % line
					return render(request, 'addman/bulk_import.html', context={'form': form, })
			notice = "Thanks for the submission. Those addresses have been imported."
			return HttpResponseRedirect(reverse('addman:all_addresses'), )
	
	else: # GET
		form = BulkImportForm()
		return render(request, 'addman/bulk_import.html', context={'form': form,} )
