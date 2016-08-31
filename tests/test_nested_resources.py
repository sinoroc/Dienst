""" Test for URI parameters
"""


# pylint: disable=duplicate-code


import unittest

import pyramid.testing
import webtest


def get_foo(dummy_context, dummy_request):
    """ View callable for top-level resource
    """
    return {
        'uri': '/foo',
    }


def get_bar(dummy_context, dummy_request):
    """ View callable for nested resource
    """
    return {
        'uri': '/foo/bar',
    }


class TestNestedResources(unittest.TestCase):
    """ Test cases for nested resources
    """

    def setUp(self):
        self.config = pyramid.testing.setUp(
            settings={
                'dienst.config.raml.title': 'test nested resources',
            },
        )
        self.config.include('dienst.config')
        self.config.add_resource(
            'foo',
            '/foo',
            display_name='Foo',
        )
        self.config.add_resource(
            'bar',
            '/foo/bar',
            display_name='Bar',
        )
        self.config.add_endpoint(
            name='foo',
            request_method='GET',
            view=get_foo,
        )
        self.config.add_endpoint(
            name='bar',
            request_method='GET',
            view=get_bar,
        )
        self.test_application = webtest.TestApp(self.config.make_wsgi_app())
        return None

    def tearDown(self):
        pyramid.testing.tearDown()
        return None

    def test_get_foo(self):
        """ Test for root-level resource
        """
        response = self.test_application.get(
            '/foo',
            status=200,
        )
        self.assertEqual(response.json['uri'], '/foo')
        return None

    def test_get_bar(self):
        """ Test for nested resource
        """
        response = self.test_application.get(
            '/foo/bar',
            status=200,
        )
        self.assertEqual(response.json['uri'], '/foo/bar')
        return None


# EOF
