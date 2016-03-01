from pyusps import address_information


class AddressValidator(object):
    def __init__(self, address: str):
        self.address = address

    def validate(self, address: str) -> Dict[str: str]:
        return {
            'status': 'matched',

            'address': '',
            'city': '',
            'state': '',
            'zip5': '',
            'zip4': ''
        }


class UspsValidator(AddressValidator):

    # from zips import zip_city_names
    # from states import state_city_names
    def __init__(self, address: str):
        super(self, AddressValidator).__init__()

    def validate(self, address: str) -> Dict[str: str]:
        line1, city = citysplit(address)
        return poll_usps([line1, city])

    def split_trailing_zip(self, address):
        # sample input: "13749 sylvan street #4 van nuys ca 91401"
        # If the address ends in a zip code:
        #   If the zip code is valid:
            #   split and return (address, zip code)
        #   If the zip code is invalid:
            #   raise valueerror
        #
        return {'zip': '91401', # or None
                'remainder': "13749 sylvan street #4 van nuys ca"
                }

    def split_trailing_state(self, address):
        # sample input: "13749 sylvan street #4 van nuys ca"
        # If the address ends in a state:
        # split and return the state and address
        return {'state': 'ca',  # or None
                'remainder': '13749 sylvan street #4 van nuys'
        }

    def split_trailing_city(self, address, state=None, zip=None):
        # It's not this method's job to figure out whether there's enough info.
        # By the time it's called, the caller can assume that there's enough
            # info.

        # if zip:
            # return split_trailing_city_with_zip()
        # if state:
            # return split_trailing_city_with_state()

    def split_trailing_city_with_zip(self, address, zip):
        # Look up the zip in the database
        # recursively_match_trailing_words in the address against the cities
            # matching the zip

    def split_trailing_city_with_state(self, address, state):
        # Look up the state in the database
        # recursively_match_trailing_words in the address against the cities
            # matching the state

    def recursively_match_trailing_words(self, address, options):
        # while no match:
            # increase the number of trailing words consumed by 1
            # check whether the set matches anything in options
        # return the match and the remainder

    def citysplit(self, address):
        # Attempt to extract the zip code
        # Attempt to extract the state
        # Attempt to extract the city
        # return the address, split in to line 1 and line 2
        pass

    def poll_usps(self, address):
        # requires the street address and one of these combos for 'city':
        # - city, state, zip
        # - city, state
        # - city, zip
        # - state, zip
        # - zip
        pass
