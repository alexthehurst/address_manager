from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Address
from .forms import BulkImportForm, AddressSetSelectForm, AddressUpdateForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
import json


# Create your views here.
class AddressDetailView(generic.DetailView):

    model = Address
    template_name = 'addman/address_detail.html'

    def get_context_data(self, **kwargs):
        # per https://docs.djangoproject.com/en/1.8/topics/class-based-views
        # /generic-display/
        context = super(AddressDetailView, self).get_context_data(**kwargs)
        context['address_update_form'] = AddressUpdateForm()  # unbound
        return context


def validate(request, pk):
    address = get_object_or_404(Address, pk=pk)
    address.validate()
    return HttpResponseRedirect(reverse('addman:address_detail',
                                            args=(address.id,)))


def validate_async(request, pk):
    address = get_object_or_404(Address, pk=pk)
    address.validate()
    # data = serializers.serialize('json', Address.objects.filter(id=pk))
    # return data
    # return JsonResponse(address, safe=False)

    data = {
        'id': pk,
        'str': str(address),
        'status': address.status,
        'message': address.message,
        'street': address.street,
        'city': address.city,
        'state': address.state,
        'zip5': address.zip5,
        'zip4': address.zip4,
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

def confirm(request, pk):
    address = get_object_or_404(Address, pk=pk)
    address.confirm_partial_match()
    return HttpResponseRedirect(reverse('addman:address_detail',
                                        args=(address.id,)))

def confirm_async(request, pk):
    address = get_object_or_404(Address, pk=pk)
    address.confirm_partial_match()
    data = {
        'id': pk,
        'status': address.status,
        'message': address.message,
        'str': str(address),
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


def update_address(request, pk):
    if request.method == 'POST':
        address = get_object_or_404(Address, pk=pk)
        address.set_user_input(request.POST['user_input'])
        return HttpResponseRedirect(reverse('addman:address_detail',
                                            args=(address.id,)))


class AllAddressesView(generic.ListView):
    template_name = 'addman/all_addresses.html'
    context_object_name = 'all_addresses_list'

    def get_queryset(self):
        """Return all the addresses in the database by default, or only the
        ones in the specified set."""
        request = self.request
        if 'address_set_select' in request.GET:
            form = AddressSetSelectForm(request.GET)

            if not form.is_valid():
                return Address.objects.none()
            # return rows
            if form.cleaned_data['address_set_select'] == 'All':
                return Address.objects.all()
            else:
                return Address.objects.filter(address_set_id=
                                              form.cleaned_data[
                                                  'address_set_select'])
        else:
            return Address.objects.none()

    def get_context_data(self, **kwargs):
        # per https://docs.djangoproject.com/en/1.8/topics/class-based-views
        # /generic-display/
        context = super(AllAddressesView, self).get_context_data(**kwargs)

        if 'address_set_select' in self.request.GET:
            form = AddressSetSelectForm(self.request.GET)
        else:
            form = AddressSetSelectForm()  # unbound

        context['address_set_select_form'] = form
        return context


def bulk_import_view(request):
    if request.method == 'POST':
        form = BulkImportForm(request.POST)
        if not form.is_valid():
            return render(request,
                          'addman/bulk_import.html',
                          context={'form': form,})
        else:
            user_bulk_import = form.cleaned_data['bulk_addresses']
            user_lines = user_bulk_import.strip().split('\n')
            address_set_id = form.cleaned_data['address_set_select'].pk
            for line in user_lines:
                try:
                    Address.objects.create(user_input=line,
                                           address_set_id=address_set_id
                                           )
                except:
                    messages.error(request, "There was an error"
                                            "importing addresses. The import "
                                            "was"
                                            "stopped at:\n'%s'." % line)
                    return render(request,
                                  'addman/bulk_import.html',
                                  context={'form': form,},
                                  )
            messages.success(request, "Thanks for the submission. "
                                      "Those addresses have been imported.")
            return HttpResponseRedirect(reverse('addman:all_addresses'))

    else:  # GET
        form = BulkImportForm()
        return render(request,
                      'addman/bulk_import.html',
                      context={'form': form,}
                      )
