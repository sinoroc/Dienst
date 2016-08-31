""" Test for URI parameters
"""


# pylint: disable=duplicate-code


import unittest

import pyramid.testing
import webtest


def get_foo(dummy_context, request):
    """ View callable
    """
    return {
        'uri_parameter': request.matchdict['uri_parameter'],
    }


class TestUriParameters(unittest.TestCase):
    """ Test cases for URI parameters
    """

    def setUp(self):
        self.config = pyramid.testing.setUp(
            settings={
                'dienst.config.raml.title': 'Test URI parameters',
            },
        )
        self.config.include('dienst.config')
        self.config.add_resource(
            'foo',
            '/foo/{uri_parameter}',
            display_name='Foo',
            uri_parameters={
                'uri_parameter': {
                    'type': 'string',
                },
            },
        )
        self.config.add_endpoint(
            view=get_foo,
            request_method='GET',
            name='foo',
        )
        self.test_application = webtest.TestApp(self.config.make_wsgi_app())
        return None

    def tearDown(self):
        pyramid.testing.tearDown()
        return None

    def test_get_foo(self):
        """ Test case for URI parameters
        """
        some_value = 'random'
        response = self.test_application.get(
            '/foo/{uri_parameter}'.format(
                uri_parameter=some_value,
            ),
            status=200,
        )
        self.assertEqual(response.json['uri_parameter'], some_value)
        return None


# EOF
