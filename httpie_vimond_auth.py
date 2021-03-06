import datetime
import base64
import hashlib
import hmac
import pytz

from httpie.plugins import AuthPlugin

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

__version__ = '0.0.1'
__author__ = 'Johan Dewe'
__licence__ = 'MIT'


class VimondAuth:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key.encode('ascii')

    def __call__(self, r):
        method = r.method

        httpdate = r.headers.get('date')
        if not httpdate:
            now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
            httpdate = now.strftime('%a, %d %b %Y %H:%M:%S %z')
            r.headers['Date'] = httpdate

        url = urlparse(r.url)
        path = url.path

        string_to_sign = '\n'.join([method, path, httpdate]).encode('utf-8')
        digest = hmac.new(self.secret_key, string_to_sign, hashlib.sha1).digest()
        signature = base64.encodestring(digest).rstrip().decode('utf-8')

        if self.api_key == '':
            raise ValueError('API key (user) cannot be empty.')
        elif self.secret_key == '':
            raise ValueError('Secret key (password) cannot be empty.')
        else:
            r.headers['Authorization'] = 'SUMO %s:%s' % (self.api_key, signature)

        return r


class VimondAuthPlugin(AuthPlugin):

    name = 'Vimond API auth'
    auth_type = 'vimond'
    description = 'Sign requests with a SUMO header, specific for Vimond API'

    def get_auth(self, username=None, password=None):
        return VimondAuth(username, password)
