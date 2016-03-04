import requests

from django_project import settings
from pyusps import address_information

FAILED = 'FAILED'
UNSUBMITTED = 'UNSUBMITTED'
MAPPED = 'MAPPED'
MAPPED_PARTIAL = 'MAPPED_PARTIAL'
MATCHED = 'MATCHED'
MATCHED_PARTIAL = 'MATCHED_PARTIAL'


class GoogleUspsValidator(object):
    # TODO: The instance variables got out of control here.
    # I'd like to refactor this to pass around return values instead of holding
    # instance variables.
    def __init__(self, user_input):
        self.key = settings.GOOGLE_API_KEY
        self.status = ''
        self.message = ''
        self.user_input = user_input

        # Expect this to be the big messy dict returned by Google API.
        self.mapped_address = {}
        self.mapped_lines = ()

        self.matched_street = ''
        self.matched_city = ''
        self.matched_state = ''
        self.matched_zip5 = ''
        self.matched_zip4 = ''

    def validate(self):

        self.google_geocode()

        if self.status in [MAPPED, MAPPED_PARTIAL]:
            self.extract_lines_from_google_address()
            self.usps_validate()

    def mapped(self, mapped_address):
        # Found a good match with Google Maps, but haven't done USPS yet.
        self.status = MAPPED
        self.mapped_address = mapped_address

    def failed(self, message):
        # The user_input is not going to be resolvable as entered.
        self.status = FAILED
        self.message = message

    def unsubmitted(self, message):
        # We haven't had a valid gmaps response about this user_input yet.
        # Most likely an API call failed entirely.
        self.status = UNSUBMITTED
        self.message = message

    def mapped_partial(self, message, mapped_address):
        # Partial match from the Google Maps API.
        self.status = MAPPED_PARTIAL
        self.message = message
        self.mapped_address = mapped_address

    def matched_partial(self, result, message):
        self.matched(result, message)
        self.status = MATCHED_PARTIAL

    def matched(self, result, message):
        self.matched_street = result['address'].title()
        self.matched_city = result['city'].title()
        self.matched_state = result['state']
        self.matched_zip5 = result['zip5']
        self.matched_zip4 = result['zip4'] or ''

        self.message = message
        self.status = MATCHED

    def google_geocode(self):

        params = {
            'address': self.user_input,
            'key': self.key,
        }
        url = 'https://maps.googleapis.com/maps/api/geocode/json'

        # noinspection PyBroadException
        try:
            response = requests.get(url, params=params).json()
        except:
            self.unsubmitted('Failed to connect to Google API. Possibly try '
                             'again later.')
            return

        if response['status'] == 'OK':
            results = response['results']

            # ROOFTOP results are the most specific. Prefer them.
            rooftops = [result for result in results
                        if result['geometry']['location_type'] == 'ROOFTOP']
            if rooftops:
                results = rooftops

            # Too many results
            if len(results) > 1:
                self.failed('Multiple results found with the Google Maps API. '
                            'Try being more specific.')
                return

            # One result
            else:
                address = results[0]

                if ('partial_match' in address or
                            address['geometry']['location_type'] in
                            ['RANGE_INTERPOLATED', 'APPROXIMATE']):
                    self.mapped_partial(
                        'Inexact match. Be sure to check the result address '
                        'carefully.',
                        address)
                    return

                elif address['geometry']['location_type'] in \
                        ['GEOMETRIC_CENTER']:
                    self.failed('Address given was too broad. Try adding more '
                                'specific detail.')
                    return

                else:
                    assert (
                        ('partial_match' not in address) and
                        (address['geometry']['location_type'] == 'ROOFTOP'))

                    # Finally!
                    self.mapped(address)
                    return

        # Bad status
        else:

            if response['status'] == 'ZERO_RESULTS':
                self.failed('No results found with the Google Maps API.')
                return

            else:  # Other error code

                message = ('Google API call failed with status {}. ({})'.format(
                    response['status'],
                    response.get('error_message',
                                 'No additional error message.'))
                )

                self.unsubmitted(message)
                return

    def extract_lines_from_google_address(self):
        relevant_types = {'street_number',  # Street name
                          'route',  # Street name
                          'subpremise',  # Apartment number
                          'administrative_area_level_1',  # State
                          'locality',  # City
                          'postal_code',  # ZIP
                          }

        my_components = {}

        for gmap_component in self.mapped_address['address_components']:
            component_types = gmap_component['types']
            my_types = relevant_types.intersection(component_types)

            if my_types:
                # If this isn't true then I'm making bad assumptions about
                # the API:
                assert len(my_types) == 1

                my_type = my_types.pop()
                my_components[my_type] = gmap_component['long_name']

        # Concatenate only the elements which are not empty. Can't predict
        # which ones the Google API will return.
        line_1 = ' '.join(
            filter(
                lambda x: x is not None,
                [
                    my_components.get('street_number'),
                    my_components.get('route'),
                    my_components.get('subpremise'),
                ]
            )
        )
        line_2 = ' '.join(
            filter(
                lambda x: x is not None,
                [
                    my_components.get('locality'),
                    my_components.get('administrative_area_level_1'),
                    my_components.get('postal_code'),
                ]
            )
        )

        self.mapped_lines = (line_1, line_2)

    def usps_validate(self):

        line_1, line_2 = self.mapped_lines

        key = settings.USPS_API_KEY

        data = {
            'address': line_1,
            'city': line_2
        }

        result = {}

        try:
            result = address_information.verify(key, data)
        except ValueError as e:
            self.failed(e.message)
            return

        if result.get('returntext'):
            self.matched_partial(result, "(USPS): " + result.get('returntext'))

        # Good USPS match, partial Google match
        elif self.status == MAPPED_PARTIAL:
            self.matched_partial(result, self.message)

        else:
            assert (self.status == MAPPED)  # Belt and suspenders
            self.matched(result, "Address is fully matched and is deliverable.")
