import simplejson as json
import datetime
import sys

DEFAULT_DATE_FORMAT = '%a, %d %b %Y %H:%M:%S UTC'
DEFAULT_ARGUMENT = "datetime_format"
DEFAULT_FUNCTION = "convert_function"


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring


def get_default_convert_function(format):
    return lambda v, func: datetime.datetime.strptime(v, format)


def loads(s, **kwargs):
    format = kwargs.pop(DEFAULT_ARGUMENT, None) or DEFAULT_DATE_FORMAT
    default_convert_func = get_default_convert_function(format)
    user_convert_func = kwargs.pop(DEFAULT_FUNCTION, None) or (lambda v, f: f(v, None))
    convert_func = lambda v, f: user_convert_func(v, default_convert_func)
    source = json.loads(s, **kwargs)
    return iteritems(source, format, convert_func)


def iteritems(source, format, convert_func):
    if isinstance(source, list):
        for k, v in enumerate(source):
            source[k] = iteritems(v, format, convert_func)
    elif isinstance(source, dict):
        for k, v in source.items():
            source[k] = iteritems(v, format, convert_func)
    elif isinstance(source, string_types):
            try:
                return convert_func(source, None)
            except Exception as e:
                None
    return source
