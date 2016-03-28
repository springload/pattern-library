# Pattern Library

This is some _very_ initial thinking about how a pattern library could work.

The folder structure isn't right. And it doesn't do much for now. But it's a start.

## Installation

In `PROJECT/settings.py`:
 - Add `patterns` to `INSTALLED_APP`
 - Add `os.path.join(BASE_DIR, 'patterns', 'components')` to `TEMPLATES['DIRS']`

## Syntax

You load some data and pass it to a component.

This could be stored in a Python package:

```
{% component "button" data='example.conf.DEFAULT_BUTTON' %}
```

Set dynamically in the template:

```twig
{% options button_data %}
  {
    "class": [
      "btn",
      "btn-primary",
      "btn-options"
    ],
    "attrs": {
        "data-button": "some-value"
    },
    "label": "{{ 'I changed the label' }}"
  }
{% endoptions %}
{% component "button" data=button_data %}
```

Or both:


```twig
{% load_data "example.data.BUTTON_DATA" as common_data %}
{% options common_data button_data %}
  {
    "label": "{{ 'I changed the label' }}"
  }
{% endoptions %}
{% component "button" data=button_data  %}
```

## Custom components

### Setup your own app
1. Create a new application `./manage.py startapp my_app`
1. Update `PROJECT/settings.py`:
  - Add `my_app` to `INSTALLED_APP` **before** `patterns`
  - Add `os.path.join(BASE_DIR, 'my__app', 'components')` to `TEMPLATES['DIRS']` **before** `os.path.join(BASE_DIR, 'patterns', 'components')`

### Create new components
Use `./manage.py createcomponent my_app my_component` to scafold the basic structure under `my_app/components/`

## Starting the server

`./manage.py runserver`
