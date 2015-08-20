from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Address
from django.utils import timezone
import datetime

# Create your tests here.

class AddressMethodTests(TestCase):
	def test_can_create_address(self):
		"""
		It should be possible to save an address to the DB.
		"""
		address=Address.objects.create(user_input="13749 Sylvan St. #1, Ellwood, CO 45371")
	def test_address_creation_time_defaults_to_now(self):
		before_time = timezone.now()
		address=Address.objects.create(user_input="13749 Sylvan St. #1, Ellwood, CO 45371")
		self.assertLess(before_time, address.creation_time)
		self.assertLess(address.creation_time, timezone.now())


class AllAddressViewTests(TestCase):
	def test_all_address_view_loads_when_no_data(self):
	 	"""
	 	When there aren't any addresses, all_address_view should show 
		a notice of such.
	 	"""
		response = self.client.get(reverse('addman:all_addresses'))
		self.assertEqual(response.status_code, 200) 
		self.assertContains(response, 'No addresses are available.')
	def test_all_address_view_shows_multiple_addresses(self):
		"""
		When there are addresses, all_address_view should show all of them.
		"""
		raise RuntimeError, "This test hasn't been written."


class BulkImportViewTests(TestCase):
	def test_bulk_import_view_with_get_shows_input_form(self):
		"""
		When given a GET request, the bulk_import view should return a
		page with a form for pasting.
		"""
		raise RuntimeError, "This test hasn't been written."
	def test_bulk_import_too_many_lines_gives_error(self):
		"""
		If there are more than 500 addresses, the bulk importer should give 
		an error.
		"""
		raise RuntimeError, "This test hasn't been written."

	def test_bulk_import_too_many_chars_gives_error(self):
		"""
		The 40,000 character limit is generous. If there's more than that 
		many chars, something is wrong.
		"""
		raise RuntimeError, "This test hasn't been written."
	def test_bulk_import_posting_data_works(self):
		"""
		POSTing some bulk address data should create DB records.
		"""
		raise RuntimeError, "This test hasn't been written."
	def test_bulk_import_posting_multiple_times_adds_data(self):
		"""
		POSTing bulk addresses when address data already exists should add, not overwrite.
		"""
		raise RuntimeError, "This test hasn't been written."
