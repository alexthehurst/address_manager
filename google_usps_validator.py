import requests
from django.conf import settings

FAILED = 'FAILED'
CONDITIONAL = 'CONDITIONAL'
MAPPED = 'MAPPED'
UNSUBMITTED = 'UNSUBMITTED'


class GoogleUspsValidator(object):
    def __init__(self):
        self.key = settings.GOOGLE_API_KEY

    def validate(self, address):
        return self.google_geocode(address)
        # self.data = {
        #     'street': '556 Main St.',
        #     'city': 'Milford',
        #     'state': 'ID',
        #     'zip': '11111',
        # }
        #
        # self.message = 'Nice looking address!'
        # self.status = 'CONFIRM'

    def google_geocode(self, raw_address):

        params = {
            'address': raw_address,
            'key': self.key,
        }
        url = 'https://maps.googleapis.com/maps/api/geocode/json'

        # Defaults
        status = FAILED
        message = ''
        address = []

        try:
            response = requests.get(url, params=params).json()
        except:
            response = {
                'status': UNSUBMITTED,
                'error_message': "Unable to get a response from the Google "
                                 "API server."
            }
            message = 'Failed to connect to Google API. Possibly try again ' \
                      'later.'

        if response['status'] == 'OK':

            # One result
            if len(response['results']) == 1:

                result = response['results'][0]

                if ('partial_match' in result or
                        result['geometry']['location_type'] in [
                        'RANGE_INTERPOLATED',
                        'APPROXIMATE'
                        ]):
                    status = CONDITIONAL
                    message = 'Inexact match. Be sure to check the result ' \
                              'address carefully.'
                    address = result

                elif result['geometry']['location_type'] in \
                        ['GEOMETRIC_CENTER']:
                    message = 'Address given was too broad. Try adding more ' \
                              'specific detail.'

                else:
                    assert (
                        ('partial_match' not in result) and
                        (result['geometry']['location_type'] == 'ROOFTOP'))
                    status = MAPPED
                    address = response['results'][0]

            # Too many results
            else:
                assert (len(response['results']) > 1)
                message = 'Multiple results found with the Google Maps API. ' \
                          'Try being more specific.'

        # Bad status
        else:

            assert (response['status'] != 'OK')

            if response['status'] == 'ZERO_RESULTS':
                message = 'No results found with the Google Maps API.'

            elif response['status'] == 'UNSUBMITTED':
                status = response['status']

            else:  # Other error code
                status = UNSUBMITTED
                message = 'Google API call failed with status %s.' % response[
                    'status']

            if 'error_message' in response:
                message += ' (Error message: %s)' % response[
                    'error_message']

        return {
            'status': status,
            'message': message,
            'address': address
        }
