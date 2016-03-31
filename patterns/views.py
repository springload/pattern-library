import collections

from django.shortcuts import render
from django.conf import settings

from components import refresh
from components.base import registry


def get_all():
    reg = collections.OrderedDict(sorted(registry.items()))
    reg.pop('BaseComponent', None)
    reg.pop('MissingComponent', None)
    return reg


def all(request):
    if settings.DEBUG:
        refresh()

    context = {
        'components': get_all()
    }

    return render(request, 'patterns/index.html', context)


def one(request, component_name):
    if settings.DEBUG:
        refresh()

    context = {
        'components': get_all(),
        'foo': registry[component_name],
        'name': registry[component_name].__name__
    }

    return render(request, 'patterns/one.html', context)


# Create your views here.
def examples(request):
    return render(request, 'patterns/examples.html', {
        'button_data': {
            'label': 'A button',
            'type': 'Primary'
        },
        'alert_data': {
            'content': 'This is the alert'
        },
        'donation_amounts': {
            'name': 'donations',
            'options': [
                {
                    'name': 'donations',
                    'value': 50,
                    'label': '$50'
                },
                {
                    'name': 'donations',
                    'value': 75,
                    'label': '$75'
                },
                {
                    'name': 'donations',
                    'value': 200,
                    'label': '$200'
                }
            ]
        }
    })
