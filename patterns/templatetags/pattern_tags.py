from django import template
from django.template import Context, Node
import sys
import patterns.components
from patterns.base_component import BaseComponent
import importlib

register = template.Library()


def get_class(name):
    try:
        return getattr(patterns.components, name)
    except KeyError:
        raise template.TemplateSyntaxError("Component class '%s' not found" % name)


class Component(Node):
    def __init__(self, component_name, **kwargs):
        self.component_name = component_name
        self.arguments = kwargs

        if 'data' in kwargs:
            self.data = kwargs['data']

        if 'config' in kwargs:
            self.config = kwargs['config']

    def get_config(self):
        conf_path = '.'.join(self.config.split('.')[:-1])
        dict_name = self.config.split('.')[-1]

        try:
            module = importlib.import_module(conf_path)
        except:
            module = BaseComponent
            print "Warning: Module %s doesn't exist" % conf_path

        attrs = {}

        try:
            attrs = module.__dict__[dict_name]
        except KeyError as e:
            raise e

        return attrs

    def get_data(self):
        if hasattr(self, 'data'):
            print "get_data ^^^"
            print self.data
            return self.data
        else:
            return {}

    def render(self, context):
        component_class = self.component_name.replace("_", " ").title().replace(" ", "")
        _class = get_class(component_class)

        if hasattr(self, 'data'):
            print 'self.data:'
            print self.data

        if hasattr(self, 'config'):
            config = self.get_config()

        instance = _class(self.component_name, context, config, self.get_data())

        return instance.render(Context({'arguments': self.arguments}, autoescape=context.autoescape))


@register.simple_tag(takes_context=True)
def component(context, component_name, **kwargs):
    component = Component(component_name, **kwargs)
    return component.render(context)
