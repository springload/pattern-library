import json
import importlib

from django import template
from django.template import Context, Node
from django.utils.safestring import mark_safe

from patterns.components.base import get_class


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
        _class = get_class(self.component_name)
        instance = _class(context, self.get_data())
        return instance.render(Context({'arguments': self.arguments}, autoescape=context.autoescape))


@register.assignment_tag
def load_data(path):
    return load_dict(path)


@register.simple_tag(takes_context=True)
def component(context, component_name, **kwargs):
    return Component(component_name, **kwargs).render(context)


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

    def __init__(self, option_name, nodelist):
        self.option_name = option_name
        self.nodelist = nodelist

    def render(self, context):
        node_content = self.nodelist.render(context)
        context[self.option_name] = json.loads(node_content)
        return ''


@register.simple_tag
def jsonify(var):
    return json.dumps(var, indent=2)


@register.tag
def options(parser, token):
    option_name = token.split_contents()[-1]

    nodelist = parser.parse(('endoptions',))
    parser.delete_first_token()

    return OptionNode(option_name, nodelist)


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
