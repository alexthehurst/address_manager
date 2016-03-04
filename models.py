from django.db import models
from django.utils import timezone
from addman.google_usps_validator import GoogleUspsValidator


# Create your models here.

class AddressSet(models.Model):
    set_name = models.CharField(max_length=150)
    set_description = models.CharField(max_length=1000, blank=True)
    creation_time = models.DateTimeField('date created', default=timezone.now)
    update_time = models.DateTimeField('date updated', default=timezone.now)
    owner = models.CharField(max_length=30)

    def __str__(self):
        return self.set_name


class Address(models.Model):
    UNSUBMITTED = 'UNSUBMITTED'
    FAILED = 'FAILED'
    MATCHED_PARTIAL = 'MATCHED_PARTIAL'
    MATCHED = 'MATCHED'

    STATUS_CHOICES = (
        (UNSUBMITTED, 'Not yet processed'),
        (FAILED, 'No match found'),
        (MATCHED_PARTIAL, 'Tentative match, confirmation required'),
        (MATCHED, 'Validated and deliverable'),
    )

    creation_time = models.DateTimeField('date created', default=timezone.now)
    address_set = models.ForeignKey(AddressSet)
    user_input = models.CharField(max_length=1000)

    street = models.CharField(blank=True, max_length=1000)
    city = models.CharField(blank=True, max_length=1000)
    state = models.CharField(blank=True, max_length=2)
    zip5 = models.CharField(blank=True, max_length=5)
    zip4 = models.CharField(blank=True, max_length=4)

    status = models.CharField(max_length=50,
                              choices=STATUS_CHOICES,
                              default=UNSUBMITTED)

    message = models.TextField(blank=True)

    def __str__(self):
        return self.user_input

    def validate(self):

        validator = GoogleUspsValidator(self.user_input)
        validator.validate()

        self.status = validator.status
        self.message = validator.message

        self.street = validator.matched_street
        self.city = validator.matched_city
        self.state = validator.matched_state
        self.zip5 = validator.matched_zip5
        self.zip4 = validator.matched_zip4

        if self.status in ['MAPPED_PARTIAL', 'MAPPED']:
            self.street = validator.address['formatted_address']
        else:
            self.street = self.message
        self.save()


        # self.street = processed_address.data['street']
        # self.city = processed_address.data['city']
        # self.state = processed_address.data['state']
        # self.zip = processed_address.data['zip']
        #
        # self.validation_message = processed_address.message
        # self.status = processed_address.status

    def set_user_input(self, user_input):

        self.user_input = user_input

        self.status = self.UNSUBMITTED
        self.message = ''

        self.street = ''
        self.city = ''
        self.state = ''
        self.zip = ''
        self.save()
