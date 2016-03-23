from django.template import Node


class BaseComponent(Node):
    defaults = {}

    def __init__(self, template_name, ctx, data):
        self.template_name = template_name
        self.ctx = ctx
        self.data = data

    def set_data(self, data):
        self.data = data

    def get_data(self):
        data = {}
        if hasattr(self, 'data'):
            data.update(self.data)

        data['type'] = self.__class__.__name__
        return data

    def get_template(self, context):
        template_name = self.template_name

        if hasattr(self, 'template'):
            template_name = self.template

        self.loaded_template = self.ctx.template.engine.get_template('components/%s.html' % template_name)
        return self.loaded_template

    def render(self, context):
        context['data'] = self.get_data()
        return self.get_template(context).render(context)
