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
		address=Address.objects.create(user_input=
			"13749 Sylvan St. #1, Ellwood, CO 45371")
	def test_address_creation_time_defaults_to_now(self):
		"""
		When an address is created with no creation_time, 
		the creation_time should be right now.
		"""
		before_time = timezone.now()
		address=Address.objects.create(user_input=
			"13749 Sylvan St. #1, Ellwood, CO 45371")
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
		When there are addresses, all_address_view should show all of 
		them.
		"""
		address=Address.objects.create(user_input=
			"13749 Sylvan St. #1, Ellwood, CO 45371")
		address=Address.objects.create(user_input=
			"12345 Moo St. #48, Higgledypufftown, AK 90210")
		response = self.client.get(reverse('addman:all_addresses'))
		self.assertContains(response, "13749", status_code=200) 
		self.assertContains(response, "12345", status_code=200) 


class BulkImportViewTests(TestCase):
	sample_address = "54321 Main St. #42, Anytown, MA 12345"
	def test_bulk_import_view_with_get_shows_input_form(self):
		"""
		When given a GET request, the bulk_import view should return a
		page with a form for pasting.
		"""
		response = self.client.get(reverse('addman:bulk_import'))
		self.assertContains(response, 
			'Paste up to 500 addresses here, one per line.', 
			status_code=200)
	def test_bulk_import_too_many_lines_gives_error(self):
		"""
		If there are more than 500 addresses, the bulk importer should 
		give an error.
		"""
		response = self.client.post(reverse('addman:bulk_import'),
			data={'bulk_addresses': 501*(self.sample_address + '\n')}
		)
		self.assertContains(response, 'Sorry, bulk imports are limited to 500 rows per round.')
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
		self.assertContains(response, "necessary response text",
					status_code=302)
		raise RuntimeError, "This test hasn't been written."
	def test_bulk_import_posting_multiple_times_adds_data(self):
		"""
		POSTing bulk addresses when address data already exists should add, not overwrite.
		"""
		raise RuntimeError, "This test hasn't been written."
	
