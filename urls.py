from django.conf.urls import patterns, include, url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
	url(r'^detail/(?P<pk>[0-9]+)',
        views.AddressDetailView.as_view(),
        name='detail'
    ),
	url(r'^$',
        views.AllAddressesView.as_view(),
        name='all_addresses'
    ),
	url(r'^all_addresses/',
        views.AllAddressesView.as_view(),
        name='all_addresses'
    ),
	url(r'^bulk_import/', views.bulk_import_view, name='bulk_import'),
]
