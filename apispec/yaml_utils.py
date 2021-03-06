# -*- coding: utf-8 -*-
"""YAML utilities"""

from collections import OrderedDict
import yaml

from apispec.lazy_dict import LazyDict
from apispec.compat import PY2, unicode, iteritems
from apispec.utils import trim_docstring, dedent


class YAMLDumper(yaml.Dumper):

    @staticmethod
    def _represent_dict(dumper, instance):
        return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())

    if PY2:
        @staticmethod
        def _represent_unicode(_, uni):
            return yaml.ScalarNode(tag=u'tag:yaml.org,2002:str', value=uni)


if PY2:
    yaml.add_representer(unicode, YAMLDumper._represent_unicode, Dumper=YAMLDumper)
yaml.add_representer(OrderedDict, YAMLDumper._represent_dict, Dumper=YAMLDumper)
yaml.add_representer(LazyDict, YAMLDumper._represent_dict, Dumper=YAMLDumper)


def dict_to_yaml(dic):
    return yaml.dump(dic, Dumper=YAMLDumper)


def load_yaml_from_docstring(docstring):
    """Loads YAML from docstring."""
    split_lines = trim_docstring(docstring).split('\n')

    # Cut YAML from rest of docstring
    for index, line in enumerate(split_lines):
        line = line.strip()
        if line.startswith('---'):
            cut_from = index
            break
    else:
        return {}

    yaml_string = '\n'.join(split_lines[cut_from:])
    yaml_string = dedent(yaml_string)
    return yaml.load(yaml_string) or {}


PATH_KEYS = set([
    'get',
    'put',
    'post',
    'delete',
    'options',
    'head',
    'patch',
])

def load_operations_from_docstring(docstring):
    """Return a dictionary of OpenAPI operations parsed from a
    a docstring.
    """
    doc_data = load_yaml_from_docstring(docstring)
    return {
        key: val for key, val in iteritems(doc_data)
        if key in PATH_KEYS or key.startswith('x-')
    }
