import json
import re
import markdown2

from bs4 import BeautifulSoup
from django import template
from django.template import Context, Node
from django.utils.safestring import mark_safe

from patterns.components.utils import camel_to_snake

from patterns.components.base import get_class
from patterns.utils import dequote, is_quoted, load_dict

register = template.Library()


class ComponentNode(Node):
    def __init__(self, component_name, context, **kwargs):
        self.component_name = component_name
        self.arguments = kwargs
        _class = get_class(self.component_name)

        if 'data' in kwargs:
            self.data = kwargs['data']

        self.instance = _class(context)
        self.context = context

    def get_data(self):
        if hasattr(self, 'data'):
            if isinstance(self.data, dict):
                return self.data
            else:
                self.data = load_dict(self.data)
                return self.data
        else:
            return {}

    def render(self, context):
        ctx = Context({'arguments': self.arguments, 'data': self.get_data()}, autoescape=context.autoescape)
        return self.instance.render(ctx)


@register.simple_tag(takes_context=True)
def render_component(context, component, **kwargs):
    return component.render(context, **kwargs)


@register.assignment_tag
def load_data(path):
    return load_dict(path)


@register.simple_tag(takes_context=True)
def component(context, component_name, **kwargs):
    return ComponentNode(component_name, context, **kwargs).render(context)


@register.assignment_tag(takes_context=True)
def load_component(context, component_name, **kwargs):
    component_name = camel_to_snake(component_name)
    return ComponentNode(component_name, context, **kwargs).instance


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

    def __init__(self, option_name, nodelist, defaults_name=None):

        self.option_name = option_name
        self.nodelist = nodelist
        self.defaults_name = defaults_name

    def render(self, context):

        node_content = self.nodelist.render(context)
        data = json.loads(node_content)
        defaults = {}

        if self.defaults_name:

            # If is quoted param name, load the var:
            if (is_quoted(self.defaults_name)):
                defaults = load_dict(dequote(self.defaults_name))
            else:
                try:
                    defaults = context[self.defaults_name]
                except KeyError, e:
                    raise e

        data = merge(defaults, data)
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

    bits = token.split_contents()
    if len(bits) == 3:
        tag_name, defaults_name, option_name = bits

    elif len(bits) == 2:
        tag_name, option_name = token.split_contents()
        defaults_name = None

    else:
        raise ValueError("Incorrect number of arguments passed to options. Expecting 2 or 3.")

    nodelist = parser.parse(('endoptions',))
    parser.delete_first_token()

    return OptionNode(option_name, nodelist, defaults_name)


@register.filter(name='htmlattributes', is_safe=True, needs_autoescape=False)
def htmlattributes(hash_):
    string = ""

    if not isinstance(hash_, dict):
        return ""

    for key, val in hash_.iteritems():
        if val.startswith('\"') or val.endswith('\"'):
            continue

        string += "%s=\"%s\"" % (key, val)
    return mark_safe(string)


# ==============================================================================
# Monkey patch the BS4 prettify function
# ==============================================================================

orig_prettify = BeautifulSoup.prettify

r = re.compile(r'^(\s*)', re.MULTILINE)


def prettify(self, encoding=None, formatter="minimal", indent_width=2):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))

BeautifulSoup.prettify = prettify

# ==============================================================================


class PrettyPrintNode(Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        html = BeautifulSoup(self.nodelist.render(context), 'html.parser')
        return html.prettify()


@register.tag()
def pretty(parser, token):
    nodelist = parser.parse(('endpretty',))
    parser.delete_first_token()
    return PrettyPrintNode(nodelist)


@register.filter(is_safe=True)
def markdown(value):
    return mark_safe(markdown2.markdown(value))


@register.filter()
def snakeify(value):
    return camel_to_snake(value)
