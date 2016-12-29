from rest_framework.exceptions import MethodNotAllowed


class RequestLogMiddleware(object):
    @staticmethod
    def process_request(request):
        data = {
            'request_method': request.method,
            'http_host': request.META['HTTP_HOST'],
            'request_path': request.get_full_path(),
        }

        message = '%(method)s %(http_host)s%(path)s' % {
            'method': data['request_method'],
            'http_host': data['http_host'],
            'path': data['request_path']}

        body = ', '.join(
            ['%(key)s=%(value)s' % {'key': k, 'value': v[0]} for k, v in
             request.data.items()])

        message += ' {' + body + '}'
        return message


def build_method_not_allow_exception(request):
    return MethodNotAllowed(
        method=request.method,
        detail=('No permission to execute the request "%(request)s" '
                'by the user %(user)s.' %
                {
                    'request': RequestLogMiddleware.process_request(request),
                    'user': request.user.__str__()
                }),
        code='NoPermission')
