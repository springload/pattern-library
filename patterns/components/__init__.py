from patterns.components.utils import component_loader


component_loader(__path__, __name__)


def refresh():
    component_loader(__path__, __name__)
