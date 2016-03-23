# Pattern Library

This is some _very_ initial thinking about how a pattern library could work.

The folder structure isn't right. And it doesn't do much for now. But it's a start.

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

## Starting the server

`./manage.py runserver`
