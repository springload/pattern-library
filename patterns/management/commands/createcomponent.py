import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from patterns.components.utils import camel_to_snake, snake_to_camel


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):

        parser.add_argument('app')
        parser.add_argument('component', nargs='?', default='')

    def handle(self, *args, **options):

        # Inputs
        app_name = options['app'].strip()
        component_name = options['component'].strip()

        if app_name and component_name=='':
            component_name = app_name
            app_name = 'patterns'

        component_name = camel_to_snake(component_name)
        component_class_name = snake_to_camel(component_name)
        local_path = os.path.join(app_name, 'components', component_name)
        component_path = os.path.join(settings.BASE_DIR, local_path)

        # Handle errors
        if not app_name:
            raise CommandError('Missing app name')

        if app_name not in settings.INSTALLED_APPS:
            raise CommandError('Invalid app name')

        if not component_name:
            raise CommandError('Missing component name')

        if os.path.exists(component_path):
            raise CommandError('Component already exists at {0}'.format(component_path))

        # Create component
        os.makedirs(component_path)
        css_name = 'c-{name}'.format(name=component_name.replace('_', '-'))

        html_file = os.path.join(component_path, component_name + '.html')
        with open(html_file, 'w') as f:
            f.write("<div class='{css_name}'>\n\n</div>".format(css_name=css_name))
            f.close()

        options_file = os.path.join(component_path, 'config.yaml')
        with open(options_file, 'w') as f:
            defaults = """defaults:
  title: ''

demo:
  title: ''

schema:
  title:
    type: string
    description: "The title attribute for the {name}"
            """.format(name=component_class_name)
            f.write(defaults)
            f.close()

        style_file = os.path.join(component_path, component_name + '.scss')
        with open(style_file, 'w') as f:
            f.write('.%s {\n\n}' % css_name)
            f.close()

        readme_file = os.path.join(component_path, 'README.md')
        with open(readme_file, 'w') as f:
            f.write('## {name}'.format(name=component_class_name))
            f.close()

        python_file = os.path.join(component_path, '__init__.py')
        with open(python_file, 'w') as f:
            f.write(
                'from patterns.components.base import BaseComponent\n\n\n'
                'class {klass}(BaseComponent):\n    pass\n'.format(klass=component_class_name)
            )
            f.close()

        for p in [python_file, readme_file, style_file, options_file, html_file]:
            localised = p.replace(settings.BASE_DIR, '')[1:]
            print '[Created] {file}'.format(file=localised)
