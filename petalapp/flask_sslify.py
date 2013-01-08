# -*- coding: utf-8 -*-

from flask import request, redirect

YEAR_IN_SECS = 31536000


class SSLify(object):
    """Secures your Flask App."""

    def __init__(self, app, age=YEAR_IN_SECS, subdomains=False, permanent=False, excluded='False'):
        if app is not None:
            self.app = app
            self.hsts_age = age
            self.hsts_include_subdomains = subdomains
            self.permanent = permanent
            self.excluded = excluded

            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        """Configures the configured Flask app to enforce SSL."""
        app.before_request(self.redirect_to_ssl)
        app.after_request(self.set_hsts_header)

    @property
    def hsts_header(self):
        """Returns the proper HSTS policy."""
        hsts_policy = 'max-age={0}'.format(self.hsts_age)

        if self.hsts_include_subdomains:
            hsts_policy += '; includeSubDomains'

        return hsts_policy

    def redirect_to_ssl(self):
        """Redirect incoming requests to HTTPS."""
        # Should we redirect?
        criteria = [
            request.is_secure,
            not(self.app.debug),# FIXME just for debug
            request.headers.get('X-Forwarded-Proto', 'http') == 'https'
        ]
        print('not any criteria: ', not any(criteria))
        if not any(criteria):
            print('self.excluded: ', self.excluded)
            print('request.url: ', request.url)
            print('self.excluded not in request.url :', self.excluded not in request.url)
            print("request.url.startswith('http://') and self.excluded not in request.url",\
                    request.url.startswith('http://') and self.excluded not in request.url)
            print("style not in request: ", 'style' not in request.url)
            if request.url.startswith('http://') and ((self.excluded not in request.url) and ('style' not in request.url)):
                url = request.url.replace('http://', 'https://', 1)
                print('url: ', url)
                code = 302
                if self.permanent:
                    code = 301
                r = redirect(url, code=code)
                print('r: ', r)

                return r

    def set_hsts_header(self, response):
        """Adds HSTS header to each response."""
        response.headers.setdefault('Strict-Transport-Security', self.hsts_header)
        return response
