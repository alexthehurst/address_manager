from django.shortcuts import render
from django.views import generic
from .models import Address
from .forms import BulkImportForm, AddressSetSelectForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

# Create your views here.

class AllAddressesView(generic.ListView):
	template_name = 'addman/all_addresses.html'
	context_object_name = 'all_addresses_list'
	def get_queryset(self):
		"""Return all the addresses in the database."""
		return Address.objects.all()
    def get_context_data(self, **kwargs):
        context = super(AllAddressesView, self).get_context_data(**kwargs)
        context['address_set_select_form'] = AddressSetSelectForm() #unbound
        return context

def bulk_import_view(request):
	if request.method=='POST':
		form = BulkImportForm(request.POST)
		if not form.is_valid():
			return render(request,
						  'addman/bulk_import.html',
						   context={'form': form, })
		else:
			user_bulk_import = form.cleaned_data['bulk_addresses']
			user_lines = user_bulk_import.strip().split('\n')
			address_set_id = form.cleaned_data['address_set_select'].pk
			for line in user_lines:
				try:
					Address.objects.create(user_input=line,
						address_set_id = address_set_id
					)
				except:
					messages.error(request, "There was an error"
						"importing addresses. The import was"
						"stopped at:\n'%s'." % line)
					return render(request,
							'addman/bulk_import.html',
							context={'form': form, },
					)
			messages.success(request, "Thanks for the submission."
					"Those addresses have been imported.")
			return HttpResponseRedirect(reverse('addman:all_addresses'))
	
	else: # GET
		form = BulkImportForm()
		return render(request,
				'addman/bulk_import.html',
				context={'form': form,}
		)
