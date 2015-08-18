from django.conf.urls import patterns, include, url
from . import views

urlpatterns = [
	url(r'all_addresses/', views.AllAddressesView.as_view(), name='all_addresses'),
]
