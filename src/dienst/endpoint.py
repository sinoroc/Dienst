""" Endpoint module
"""


import inspect

import venusian

from . import raml


MODULE_NAME = __name__

ATTRIBUTE_NAME = '{}_endpoint_defaults'.format(MODULE_NAME)


class ViewCallableNotFound(Exception):
    """ No view callable could be found for this endpoint.
    """


def add_resource(config, *args, **kwargs):
    """ Add a resource
    """
    name = args[0]
    raml_util = config.registry.queryUtility(raml.IRaml)
    full_uri = raml_util.add_resource(*args, **kwargs)
    config.add_route(name, pattern=full_uri)
    return None


def add_endpoint(config, *args, **kwargs):
    """ Add an endpoint
    """
    _Endpoint(config, *args, **kwargs)
    return None


def endpoint_defaults(*args, **kwargs):
    """ Class decorator to set endpoints defaults
    """

    return _EndpointDefaultsHelper(*args, **kwargs)


class _EndpointDefaultsHelper:  # pylint: disable=too-few-public-methods
    """ Helper for decorator endpoint_defaults
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return None

    def __call__(self, decoratee):
        setattr(decoratee, ATTRIBUTE_NAME, self.kwargs)
        return decoratee


def endpoint_config(*args, **kwargs):
    """ Decorate a view callable.
    """

    return _EndpointConfigHelper(*args, **kwargs)


class _EndpointConfigHelper:
    """ Helper for decorator endpoint_config
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.venusian_info = None
        return None

    def __call__(self, decoratee):
        self.venusian_info = venusian.attach(decoratee, self.callback)
        self.kwargs['view'] = decoratee
        return decoratee

    def callback(self, scanner, dummy_name, decorated):
        """ Callback for venusian
        """
        scope = self.venusian_info.scope  # pylint: disable=no-member
        if scope == 'class':
            self.kwargs['view_class'] = decorated
            self.retrieve_defaults(getattr(decorated, ATTRIBUTE_NAME, {}))
        module = self.venusian_info.module  # pylint: disable=no-member
        config = scanner.config.with_package(module)
        add_endpoint(config, *self.args, **self.kwargs)
        return None

    def retrieve_defaults(self, defaults):
        """ Retrieve the defaults set by endpoint_defaults class decorator
        """
        for key, value in defaults.items():
            if key not in self.kwargs:
                self.kwargs[key] = value
        return None


class _Endpoint:
    """ Endpoint
    """

    def __init__(self, config, *dummy_args, **kwargs):
        resource_name = kwargs['name']
        self.user_view_callable = kwargs['view']
        self.user_view_callable_class = kwargs.get('view_class', None)
        self.request_method = kwargs['request_method']
        self.raml_util = config.registry.queryUtility(raml.IRaml)
        self.commit(config, resource_name)
        return None

    def commit(self, config, resource_name):
        """ Add the endpoint to the global RAML document
        """
        config.add_view(
            view=self.view_callable,
            route_name=resource_name,
            request_method=self.request_method,
            renderer='json',
        )
        self.raml_util.add_endpoint(
            resource_name,
            self.request_method,
        )
        return None

    def view_callable(self, *args, **kwargs):
        """ Wrapper for the user view callable
        """
        result = self.run_user_view_callable(*args, **kwargs)
        return result

    def run_user_view_callable(self, *args, **kwargs):
        """ Call the user view callable
        """
        result = None
        if self.user_view_callable_class:
            result = self.user_view_callable(
                self.user_view_callable_class(*args, **kwargs)
            )
        elif inspect.isclass(self.user_view_callable):
            result = self.user_view_callable(*args, **kwargs)()
        elif inspect.isfunction(self.user_view_callable):
            result = self.user_view_callable(*args, **kwargs)
        else:
            raise ViewCallableNotFound()
        return result


# EOF
