from builtins import object, setattr


class DisableCSRF(object):
    '''
    http://stackoverflow.com/a/4631626/1035552
    '''

    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)