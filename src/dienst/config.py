""" Package configuration
"""


import pyramid

from . import endpoint
from . import raml


PACKAGE_NAME = __name__


def includeme(config):
    """ Include into Pyramid configuration
    """
    raml_title = config.registry.settings['{}.raml.title'.format(PACKAGE_NAME)]
    config.registry.registerUtility(raml.Raml(raml_title), raml.IRaml)
    config.add_directive('add_resource', endpoint.add_resource)
    config.add_directive('add_endpoint', endpoint.add_endpoint)
    config.add_subscriber(
        raml.build_document,
        pyramid.events.ApplicationCreated,
    )
    return None


# EOF
