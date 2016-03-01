from addman.models import Address
# Why can't I import Address here? (try Running to see the error)

class GoogleUspsValidator(object):
    def __init__(self, address: Address):
        self.address = address

    def validate(self):
        self.data = {
            'street': '556 Main St.',
            'city': 'Milford',
            'state': 'ID',
            'zip': 11111,
        }

        self.message = 'Nice looking address!'
        self.status = 'CONFIRM'