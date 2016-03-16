from django.template import Node


class BaseComponent(Node):
    defaults = {}

    def __init__(self, template_name, ctx, config, data):
        self.template_name = template_name
        self.ctx = ctx
        self.config = config
        self.data = data
        print data

    def set_data(self, data):
        self.data = data

    def get_config(self):
        config = self.config.copy()
        config.update(self.defaults)
        return config

    def get_data(self):
        if hasattr(self, 'data'):
            print 'get_data'

            return self.data
        else:
            return {}

    def get_template(self, context):
        self.template = self.ctx.template.engine.get_template('components/%s.html' % self.template_name)
        return self.template

    def render(self, context):
        context['config'] = self.get_config()
        context['data'] = self.get_data()
        return self.get_template(context).render(context)
