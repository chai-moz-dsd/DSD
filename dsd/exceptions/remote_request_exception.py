class RemoteRequestException(Exception):
    def __init__(self, message=None):
        if message:
            self.default_detail = message
        super(RemoteRequestException, self).__init__()

    status_code = 503
    default_detail = "remote server is busy, please contact the admin."
