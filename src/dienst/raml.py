""" RAML utility
"""


import yaml
import zope.interface


# pylint: disable=too-few-public-methods

class IRaml(zope.interface.Interface):  # pylint: disable=inherit-non-class
    """ Interface for RAML utility
    """

# pylint: enable=too-few-public-methods


@zope.interface.implementer(IRaml)
class Raml:
    """ RAML utility
    """

    MEDIA_TYPE = 'application/raml+yaml'

    _PARAMETER_NAME_MAP = {
        'display_name': 'displayName',
        'uri_parameters': 'uriParameters',
    }

    def __init__(self, title):
        self.title = title
        self.resources = {}
        self.document = None
        return None

    def add_resource(self, name, uri, *dummy_args, **kwargs):
        """ Add a resource and return the full URI
        """
        resource = {
            'name': name,
            'uri': uri,
            'parameters': {},
            'methods': {},
        }
        full_uri = uri
        parent = kwargs.get('parent', None)
        if parent is not None:
            resource['parent'] = parent
            full_uri = self._compute_full_uri(uri, parent)
        resource['full_uri'] = full_uri
        for key, value in kwargs.items():
            if key in self._PARAMETER_NAME_MAP:
                resource['parameters'][key] = value
        self.resources[name] = resource
        return full_uri

    def _compute_full_uri(self, uri, parent):
        """ Compute the full URI for a nested resource
        """
        full_uri = self.resources[parent]['full_uri'] + uri
        return full_uri

    def add_endpoint(self, name, request_method):
        """ Add an endpoint
        """
        resource = self.resources[name]
        resource['methods'][request_method.lower()] = {}
        return None

    def _build_dict(self):
        """ Build a RAML dict
        """
        raml_dict = {
            'title': self.title,
        }
        for dummy_name, resource in self.resources.items():
            resource_dict = {}
            for method, method_value in resource['methods'].items():
                resource_dict[method] = method_value
            for parameter, parameter_value in resource['parameters'].items():
                parameter_name = self._PARAMETER_NAME_MAP[parameter]
                resource_dict[parameter_name] = parameter_value
            self._place_resource_dict(resource, resource_dict, raml_dict)
        return raml_dict

    def _place_resource_dict(self, resource, resource_dict, raml_dict):
        """ Place the resource in the RAML dict
        """
        uris = [resource['uri']]
        parent_name = resource.get('parent', None)
        while parent_name is not None:
            parent = self.resources[parent_name]
            uris.append(parent['uri'])
            parent_name = parent.get('parent', None)
        node = raml_dict
        for uri in reversed(uris):
            node = node.setdefault(uri, {})
        node.update(resource_dict)
        return None

    def build_document(self):
        """ Build RAML document
        """
        raml_dict = self._build_dict()
        self.document = '\n'.join([
            '#%RAML 1.0',
            '---',
            '{}'.format(yaml.dump(raml_dict)),
            '...  # EOF',
        ])
        return None

    def dump(self):
        """ Dump as RAML YAML
        """
        return self.document


def build_document(event):
    """ Build RAML document
    """
    raml = event.app.registry.queryUtility(IRaml)
    raml.build_document()
    return None


# EOF
