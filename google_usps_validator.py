import requests
from django.conf import settings

FAILED = 'FAILED'
UNSUBMITTED = 'UNSUBMITTED'
MAPPED = 'MAPPED'
MAPPED_PARTIAL = 'MAPPED_PARTIAL'


class GoogleUspsValidator(object):
    def __init__(self, user_input):
        self.key = settings.GOOGLE_API_KEY
        self.status = ''
        self.message = ''
        self.user_input = user_input

        # Expect this to be the big messy dict returned by Google API.
        self.mapped_address = {}

    def validate(self):

        self.google_geocode()

        if self.status in [MAPPED, MAPPED_PARTIAL]:
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

    def matched(self):
        pass

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

    def usps_validate(self):
        pass  # stub