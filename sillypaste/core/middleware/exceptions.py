import logging


class ExceptionLoggingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_exception(self, request, exception):
        logging.exception('Exception handling request for ' + request.path)

    def __call__(self, request):
        """Do nothing."""
        return self.get_response(request)
