from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Address, AddressSet
from django.utils import timezone
import datetime

# Create your tests here.

class AddmanBaseTestCase(TestCase):
	def create_address_set(self):
		return AddressSet.objects.create(set_name='Set 1', id=1)

        def create_address(self,
                user_input= "13749 Sylvan St. #1, Ellwood, CO 45371",
                address_set_id=1):
		return Address.objects.create(
			user_input=user_input,
			address_set_id=address_set_id)

class ModelRelationshipTests(AddmanBaseTestCase):
	def test_can_create_address_set(self):
		"""
		It should be possible to save an address_set to the DB.
		Also, the creation_time for the address_set should default to
		now.
		"""
		before_time = timezone.now()
		address_set = self.create_address_set()
                self.assertEqual(len(AddressSet.objects.all()), 1)
                self.assertGreater(address_set.creation_time,
                            timezone.now() - datetime.timedelta(seconds=1))
                self.assertIn('Set 1', address_set.__repr__())

                address = self.create_address()
                self.assertIn("13749 Sylvan St. #1, Ellwood, CO 45371", address.__repr__()) 
                self.assertEqual(len(Address.objects.all()), 1)
                address2 = self.create_address()
                self.assertEqual(len(Address.objects.all()), 2)
                self.assertGreater(address2.creation_time,
                            timezone.now() - datetime.timedelta(seconds=1))

	def test_can_create_address(self):
		"""
		It should be possible to save an address to the DB.
		"""
		address_set = self.create_address_set()
		address = self.create_address()

	def test_address_creation_time_defaults_to_now(self):
		"""
		When an address is created with no creation_time, 
		the creation_time should be right now.
		"""
		before_time = timezone.now()
		address = self.create_address()
		self.assertLess(before_time, address.creation_time)
		self.assertLess(address.creation_time, timezone.now())

class AllAddressViewTests(AddmanBaseTestCase):
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
		address_set = self.create_address_set()
		address1=self.create_address(user_input=
			"13749 Sylvan St. #1, Ellwood, CO 45371")
		address2=self.create_address(user_input=
			"12345 Moo St. #48, Higgledypufftown, AK 90210")
		response = self.client.get(reverse('addman:all_addresses'))
		self.assertContains(response, "13749", status_code=200) 
		self.assertContains(response, "12345", status_code=200) 


class BulkImportViewTests(AddmanBaseTestCase):

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

	def test_bulk_import_too_many_lines_restores_user_input_to_form(self):
		"""
		If a user submits a too-long form, not only should the error message show, but
		the form should be repopulated with the user's input so they can edit it.
		"""
                address_set = self.create_address_set()
		response = self.client.post(reverse('addman:bulk_import'),
			data={'bulk_addresses': 501*(self.sample_address + '\n'),
                                'address_set_select': address_set.pk}
		)
		self.assertTrue('bulk_addresses' in response.context['form'].data.keys())

	def test_bulk_import_too_many_lines_gives_error(self):
		"""
		If there are more than 500 addresses, the bulk importer should 
		give an error.
		"""
		response = self.client.post(reverse('addman:bulk_import'),
			data={'bulk_addresses': 501*(self.sample_address + '\n')}
		)
		self.assertContains(response, 'Too many records. Please provide 500 or fewer lines of address data at once')

	def test_bulk_import_posting_data_works(self):
		"""
		POSTing some bulk address data should create DB records.
		"""
                address_set = self.create_address_set()
		response = self.client.post(reverse('addman:bulk_import'),
			data={'bulk_addresses': 10*(self.sample_address + '\n'),
                                'address_set_select': address_set.pk,
                        }
		)
                self.assertEqual(len(Address.objects.all()), 10)

	def test_bulk_import_posting_multiple_times_adds_data(self):
		"""
		POSTing bulk addresses when address data already exists should add, not overwrite.
		"""
                address_set = self.create_address_set()
		response = self.client.post(reverse('addman:bulk_import'),
			data={'bulk_addresses': 10*(self.sample_address + '\n'),
                                'address_set_select': address_set.pk,
                        }
		)
		response = self.client.post(reverse('addman:bulk_import'),
			data={'bulk_addresses': 10*(self.sample_address + '\n'),
                                'address_set_select': address_set.pk,
                        }
		)
		self.assertEqual(len(Address.objects.all()), 20)
        
	def test_bulk_import_with_no_entry_gives_error(self):
		"""
		POSTing a bulk address form with no data should keep you on the same page, with 
		an error message.
		"""
		response = self.client.post(reverse('addman:bulk_import'),
			data={'bulk_addresses': ''})
		self.assertContains(response, 'This field is required.')

class MoreBulkImportViewTests(AddmanBaseTestCase):

	sample_address = "54321 Main St. #42, Anytown, MA 12345"

	def test_bulk_import_with_exception_gives_error(self):
		"""
                POSTing addresses which fail to import for any reason should keep you on the same
                page, with an error message.
		"""
		address_set = self.create_address_set()
        #import pdb; pdb.set_trace()
		response = self.client.post(
                        reverse('addman:bulk_import'), 
                        data={
                            'bulk_addresses': 1001*'F', 
                            'address_set_select': address_set.pk,
                        },
                        follow=True,
                )
		self.assertContains(response, 'There was an error importing addresses.')
		self.assertTrue('bulk_addresses' in response.context['form'].data.keys())
