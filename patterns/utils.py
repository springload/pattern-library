import importlib


def dequote(s):
    """
    If a string has single or double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.
    """
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s


def is_quoted(s):
    return (s[0] == s[-1]) and s.startswith(("'", '"'))



def load_dict(path):
    conf_path = '.'.join(path.split('.')[:-1])
    dict_name = path.split('.')[-1]

    try:
        module = importlib.import_module(conf_path)
    except:
        print "Warning: Config %s at '%s' doesn't exist" % (dict_name, conf_path)

    attrs = {}

    try:
        attrs = module.__dict__[dict_name]
    except KeyError as e:
        raise e

    return attrs
