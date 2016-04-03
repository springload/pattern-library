import os

import django
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template import Context, Engine
from django.utils.version import get_docs_version

from patterns.components.utils import camel_to_snake, snake_to_camel

IGNORED_FILE_EXTENSIONS = ('.pyo', '.pyc', '.py.class')
TEMPLATES_PATH = os.path.join(settings.BASE_DIR, 'patterns', 'conf')
COMPONENTS_PATH = os.path.join(settings.BASE_DIR, '{app_name}', 'components')

class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser):

        parser.add_argument('app')
        parser.add_argument('component', nargs='?', default='')

    def handle(self, *args, **options):

        # Inputs
        app_name = options['app'].strip()
        component_name = options['component'].strip()

        if app_name and not component_name:
            component_name = app_name
            app_name = 'patterns'

        component_name = camel_to_snake(component_name)

        components_path = COMPONENTS_PATH.format(app_name=app_name)
        component_path = os.path.join(components_path, component_name)

        # Handle errors
        if not app_name:
            raise CommandError('Missing app name')

        if app_name not in settings.INSTALLED_APPS:
            raise CommandError('Invalid app name')

        if not component_name:
            raise CommandError('Missing component name')

        if os.path.exists(component_path):
            raise CommandError(
                'Component already exists at {0}'.format(component_path))

        # Create components folder if needed
        if not os.path.exists(components_path):
            self._create_components_folder(app_name)

        # Create component
        self._create_component(app_name, component_name)

    def _create_components_folder(self, app_name):

        source_dirname = 'components_dir_template'
        source_path = os.path.join(TEMPLATES_PATH, source_dirname)

        target_dirname = 'components'
        target_path = os.path.join(settings.BASE_DIR, app_name)

        context = Context(autoescape=False)

        self._copy_template(
            source_path=source_path,
            source_dirname=source_dirname,
            target_path=target_path,
            target_dirname=target_dirname,
            context=context
        )

    def _create_component(self, app_name, component_name):

        source_dirname = 'component_template'
        source_path = os.path.join(TEMPLATES_PATH, source_dirname)

        target_dirname = component_name
        target_path = os.path.join(settings.BASE_DIR, app_name, 'components')

        context = Context({
                'component_name': component_name,
                'component_class': snake_to_camel(component_name),
                'component_css_name': 'c-{name}'.format(name=component_name.replace('_', '-'))
            },
            autoescape=False
        )

        self._copy_template(
            source_path=source_path,
            source_dirname=source_dirname,
            target_path=target_path,
            target_dirname=target_dirname,
            context=context,
            component_name=component_name
        )

    def _copy_template(
        self,
        source_path,
        source_dirname,
        target_path,
        target_dirname,
        context,
        component_name=None
    ):

        prefix_length = len(TEMPLATES_PATH) + 1

        # Walk through all the file in source path
        for root, dirs, files in os.walk(source_path):
                path_rest = root[prefix_length:]

                # Rename folder
                relative_dir = path_rest.replace(source_dirname, target_dirname)
                target_dir = os.path.join(target_path, relative_dir)
                if not os.path.exists(target_dir):
                    os.mkdir(target_dir)

                # Copy file
                for filename in files:
                    if filename.endswith(IGNORED_FILE_EXTENSIONS) or filename.startswith('.'):
                        continue

                    old_filename = new_filename = filename
                    if component_name:
                        new_filename = filename.replace('COMP_NAME', component_name)

                    old_path = os.path.join(root, old_filename)
                    new_path = os.path.join(target_dir, new_filename)

                    # Read template
                    with open(old_path, 'rb') as template_file:
                        content = template_file.read()

                    # Parse template
                    content = content.decode('utf-8')
                    template = Engine().from_string(content)
                    content = template.render(context)
                    content = content.encode('utf-8')

                    # Save file
                    with open(new_path, 'wb') as new_file:
                        new_file.write(content)

                    print '[Created] {file}'.format(file=new_path)
