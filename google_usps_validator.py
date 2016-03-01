

class GoogleUspsValidator(object):
    def __init__(self, address: str):
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