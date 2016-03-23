from functools import partial
import imp
import os

from django.conf import settings
from django.template import Node, Template

from patterns.components.utils import camel_to_snake, snake_to_camel


class BaseComponent(Node):

    def __init__(self, context, data):

        self.context = context
        self.data = data

    def set_data(self, data):
        self.data = data

    def get_data(self):

        data = {}

        if self.data:
            data.update(self.data)

        data['type'] = self.__class__.__name__

        return data

    def get_template_path(self):

        name = camel_to_snake(self.__class__.__name__)

        return '{name}/{name}.html'.format(name=name)

    def get_template(self):

        template_path = self.get_template_path()
        template = self.context.template.engine.get_template(template_path)

        return template

    def render(self, context):

        context['data'] = self.get_data()

        return self.get_template().render(context)


class MissingComponent(BaseComponent):

    def __init__(self, context, data, component_name):

        super(MissingComponent, self).__init__(context, data)
        self.component_name = component_name

    def get_template(self):

        text = '<strong>Missing Component: {0}</strong>'.format(self.component_name) if settings.DEBUG else ''
        template = Template(text)

        return template


def get_class(component_name):

    try:
        possible_paths = [
            os.path.join(app, 'components', component_name)
            for app in settings.INSTALLED_APPS
            if not app.startswith('django.')
        ]

        module_info = imp.find_module(component_name, possible_paths)
        module = imp.load_module(component_name, *module_info)

        class_name = snake_to_camel(component_name)
        class_ = getattr(module, class_name)

        return class_

    except (AttributeError, ImportError):
        return partial(MissingComponent, component_name=component_name)