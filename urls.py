from django.conf.urls import patterns, include, url
from . import views
from django.views.generic import TemplateView

urlpatterns = [

	url(r'^detail/(?P<pk>[0-9]+)',
        views.AddressDetailView.as_view(),
        name='address_detail'
    ),

    url(r'^update_address/(?P<pk>[0-9]+)/$',
        views.update_address,
        name='update_address'),

	url(r'^$',
        views.AllAddressesView.as_view(),
        name='all_addresses'
    ),

	url(r'^all_addresses/',
        views.AllAddressesView.as_view(),
        name='all_addresses'
    ),

    url(r'^validate/(?P<pk>[0-9]+)/$',
        views.validate,
        name='validate'
        ),

    url(r'^confirm/(?P<pk>[0-9]+)/$',
        views.confirm,
        name='confirm'
        ),

	url(r'^bulk_import/', views.bulk_import_view, name='bulk_import'),
]
