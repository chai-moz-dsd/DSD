
class IllegalArgumentException(Exception):
    def __init__(self, *args, **kwargs):
        self.status_code = 400
        self.error_message = 'Illegal arguments exception. %s' % kwargs.get('message')
