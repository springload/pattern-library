import re
import pkgutil
import importlib


def snake_to_camel(name):
    return name.title().replace("_", "")


def camel_to_snake(name):
    name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()


def component_loader(__path__, __name__):
    """
    Loads classes from subdirectories of a given module.
    """
    __path__ = pkgutil.extend_path(__path__, __name__)

    for importer, module_name, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
        importlib.import_module(module_name)
