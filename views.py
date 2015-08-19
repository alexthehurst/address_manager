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
		#post
		form = BulkImportForm(request.POST)
		if form.is_valid() and len(form.cleaned_data['bulk_addresses'].split('\n')) <= 500:
			#process
			return HttpResponseRedirect(reverse('addman:all_addresses'))
	else:
		form = BulkImportForm()
	return render(request, 'addman/bulk_import.html', {'form': form})
