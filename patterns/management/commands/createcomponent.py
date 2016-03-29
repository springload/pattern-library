import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from patterns.components.utils import camel_to_snake, snake_to_camel


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):

        parser.add_argument('app')
        parser.add_argument('component')

    def handle(self, *args, **options):

        # Inputs
        app_name = options['app'].strip()
        component_name = camel_to_snake(options['component'].strip())
        component_class_name = snake_to_camel(component_name)
        component_path = os.path.join(settings.BASE_DIR, app_name, 'components', component_name)

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

        html_file = os.path.join(component_path, component_name + '.html')
        open(html_file, 'w').close()

        options_file = os.path.join(component_path, component_name + '.yaml')
        open(options_file, 'w').close()

        style_file = os.path.join(component_path, component_name + '.scss')
        open(style_file, 'w').close()

        readme_file = os.path.join(component_path, 'README.md')
        with open(readme_file, 'w') as f:
            f.write('## {name}'.format(name=component_class_name))

        python_file = os.path.join(component_path, component_name + '.py')
        with open(python_file, 'w') as f:
            f.write(
                'from patterns.components.base import BaseComponent\n\n\n'
                'class {klass}(BaseComponent):\n    pass\n'.format(klass=component_class_name)
            )
