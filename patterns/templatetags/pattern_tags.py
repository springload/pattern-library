import json
import importlib

from django import template
from django.template import Context, Node
from django.utils.safestring import mark_safe

import patterns.components
from patterns.base_component import BaseComponent


register = template.Library()


def load_dict(path):
    conf_path = '.'.join(path.split('.')[:-1])
    dict_name = path.split('.')[-1]

    try:
        module = importlib.import_module(conf_path)
    except:
        print "Warning: Config %s at '%s' doesn't exist" % (dict_name, conf_path)

    attrs = {}

    try:
        attrs = module.__dict__[dict_name]
    except KeyError as e:
        raise e

    return attrs


def get_class(name):
    try:
        return getattr(patterns.components, name)
    except AttributeError:
        print "Component class '%s' not found" % name
        return BaseComponent


class Component(Node):
    def __init__(self, component_name, **kwargs):
        self.component_name = component_name
        self.arguments = kwargs

        if 'data' in kwargs:
            self.data = kwargs['data']

    def get_data(self):
        if hasattr(self, 'data'):
            if isinstance(self.data, dict):
                return self.data
            else:
                return load_dict(self.data)
        else:
            return {}

    def render(self, context):
        component_class = self.component_name.replace("_", " ").title().replace(" ", "")
        _class = get_class(component_class)

        if hasattr(self, 'data'):
            print 'self.data:', self.data

        instance = _class(self.component_name, context, self.get_data())
        return instance.render(Context({'arguments': self.arguments}, autoescape=context.autoescape))


@register.assignment_tag
def load_data(path):
    return load_dict(path)


@register.simple_tag(takes_context=True)
def component(context, component_name, **kwargs):
    component = Component(component_name, **kwargs)
    return component.render(context)


@register.assignment_tag
def load_json(blob):
    json_string = blob.replace("'", "\"")
    return json.loads(json_string)


@register.assignment_tag
def merge(x, y):
    z = x.copy()
    z.update(y)
    return z


class OptionNode(template.Node):

    def __init__(self, option_name, nodelist, dict_to_merge=False):
        self.option_name = option_name
        self.nodelist = nodelist

        if dict_to_merge:
            self.dict_to_merge = dict_to_merge

    def render(self, context):
        node_content = self.nodelist.render(context)
        data = json.loads(node_content)

        if hasattr(self, 'dict_to_merge'):
            data = merge(context[self.dict_to_merge], data)

        context[self.option_name] = data
        return ''


@register.simple_tag
def jsonify(var):
    return json.dumps(var, indent=2)


@register.tag
def options(parser, token):
    """
    Takes the contents of a block tag and attempts to parse them as JSON.

    {% options export_name %}
        {"label": "foo"}
    {% end options %}

    Can also optionally accept a first parameter, the name of a dict from the
    context that you would like to merge the parsed JSON with.

    {% options merge_dict_name export_name %}
        {"label": "foo"}
    {% end options %}

    """
    original_options = False

    try:
        name, original_options, option_name = token.split_contents()
    except ValueError:
        name, option_name = token.split_contents()
    except ValueError:
        raise ValueError("Incorrect number of arguments passed to options")

    nodelist = parser.parse(('endoptions',))
    parser.delete_first_token()

    return OptionNode(option_name, nodelist, original_options)


@register.filter(name='htmlattributes', is_safe=True, needs_autoescape=False)
def htmlattributes(hash):
    string = ""

    if not isinstance(hash, dict):
        return ""

    for key, val in hash.iteritems():
        if val.startswith('\"') or val.endswith('\"'):
            continue

        string += "%s=\"%s\"" % (key, val)
    return mark_safe(string)
