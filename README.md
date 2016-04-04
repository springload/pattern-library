# Pattern Library

[Screenshot](http://www.springload.co.nz/yk-images/be145a97bab457c98eb538fc5c3d41ef/xlarge/phpfHV0vy)


This is some _very_ initial thinking about how a pattern library could work.

The pattern library has two simple goals: 


* Reduce boilerplate and repetition between projects.
* Provide documentation about the interface/frontend. This helps when new people pick up the project. They can see what it is made of.

### What lives in the pattern library?

* Forms!
 - Fields
 - Field errors/validation
 - Message
 - Variations on forms: inline fields, stacked fields, etc...
* Things that are used on at least 2 (preferably 3) production projects. Components we *know* we will re-use. 

### Naming conventions.
  - Naming is hard.
  - Where possible, use the accessible component name/role
    - FED team to read the boring spec and come up with a few good names.
  - Use names from material or WIA or bootstrap.
  - Do a naming session on all UI projects. Should include the DES + FED + DEV + AM.
  - Meet occasionally and check SL are naming components properly.

--- 

## Installation

1. Check out the project.
2. Run `pip install -r requirements.txt` in the project root.

## Starting the server

`./manage.py runserver`


### Creating new components
Use `./manage.py createcomponent my_app my_component` to scafold the basic structure under `my_app/components/`

---

## Installing into an existing Django Project

In `PROJECT/settings.py`:
 - Add `patterns` to `INSTALLED_APP`
 - Add `os.path.join(BASE_DIR, 'patterns', 'components')` to `TEMPLATES['DIRS']`

## Syntax

You load some data and pass it to a component.

This could be stored in a Python package:

```
{% component "button" data='example.conf.DEFAULT_BUTTON' %}
```

Or, set dynamically in the template:

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

### Setup your  app
1. Create a new application `./manage.py startapp my_app`
1. Update `PROJECT/settings.py`:
  - Add `my_app` to `INSTALLED_APP` **before** `patterns`
  - Add `os.path.join(BASE_DIR, 'my__app', 'components')` to `TEMPLATES['DIRS']` **before** `os.path.join(BASE_DIR, 'patterns', 'components')`
