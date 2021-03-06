from rest_framework.authtoken.models import Token
import re

class AuthTokenMiddleware(object):
    def process_request(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token is not None:
            try:
                auth_token = Token.objects.get(key=token)
                request.auth = auth_token
                request.user = auth_token.user
            except Token.DoesNotExist:
                request.user = None
                request.auth = None
                pass
        else:
            regex = re.compile('^(?!/admin)/')
            if regex.match(request.path):
                request.user = None
                request.auth = None
