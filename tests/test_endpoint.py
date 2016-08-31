""" Test endpoint
"""


# pylint: disable=duplicate-code


import unittest

import dienst
import pyramid.testing
import webtest


def get_a(dummy_context, dummy_request):
    """ View callable
    """
    return {}


@dienst.endpoint.endpoint_config(name='b', request_method='GET')
def get_b(dummy_context, dummy_request):
    """ View callable
    """
    return {}


@dienst.endpoint.endpoint_config(name='c', request_method='GET')
class GetC:  # pylint: disable=too-few-public-methods
    """ View callable
    """

    def __init__(self, context, request):
        pass

    def __call__(self):
        return {}


@dienst.endpoint.endpoint_defaults(name='d')
class GetD:  # pylint: disable=too-few-public-methods
    """ Group of view callables
    """

    def __init__(self, context, request):
        pass

    @dienst.endpoint.endpoint_config(request_method='GET')
    def get_d(self):  # pylint: disable=no-self-use
        """ View callable
        """
        return {}


class TestEndpoint(unittest.TestCase):
    """ Test cases for endpoint
    """

    def setUp(self):
        self.config = pyramid.testing.setUp(
            settings={
                'dienst.config.raml.title': 'test endpoints',
            },
        )
        self.config.include('dienst.config')
        self.config.add_resource('a', '/a', display_name='A')
        self.config.add_resource('b', '/b', display_name='B')
        self.config.add_resource('c', '/c', display_name='C')
        self.config.add_resource('d', '/d', display_name='D')
        self.config.add_endpoint(
            name='a',
            request_method='GET',
            view=get_a,
        )
        self.config.scan('.')
        self.test_application = webtest.TestApp(self.config.make_wsgi_app())
        return None

    def tearDown(self):
        pyramid.testing.tearDown()
        return None

    def test_get_a(self):
        """ Test case
        """
        self.test_application.get('/a', status=200)
        return None

    def test_get_b(self):
        """ Test case
        """
        self.test_application.get('/b', status=200)
        return None

    def test_get_c(self):
        """ Test case
        """
        self.test_application.get('/c', status=200)
        return None

    def test_get_d(self):
        """ Test case
        """
        self.test_application.get('/d', status=200)
        return None


# EOF
