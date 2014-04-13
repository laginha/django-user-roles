from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import importlib


__version__ = '0.1.0'


_IMPORT_FAILED = "Could not import role profile '%s'"
_INCORRECT_ARGS = "USER_ROLES should be a list of strings and/or two-tuples"


def _import_class_from_string(class_path):
    """
    Given a string like 'foo.bar.Baz', returns the class it refers to.
    If the string is empty, return None, rather than raising an import error.
    """
    if not class_path:
        return None
    module_path, class_name = class_path.rsplit('.', 1)
    return getattr(importlib.import_module(module_path), class_name)


class Role(object):
    """
    A single role, eg as returned by `roles.moderator`.
    """
    
    def __cmp__(self, other):
        if self.order > other.order:
            return 1
        elif self.order < other.order:
            return -1
        return 0

    def __init__(self, name, order=None):
        self.name = name
        self.order = order

    def __unicode__(self):
        return self.name


class Roles(object):

    @property
    def choices(self):
        """
        Return a list of two-tuples of role names, suitable for use as the
        'choices' argument to a model field.
        """
        return [(role, role) for role in self._config]

    def __init__(self, config=None):
        """
        By default the Roles object will be created using configuration from
        the django settings file, but you can also set the configuration
        explicitly, for example, when testing.
        """
        self._config = config or getattr(settings, 'USER_ROLES', ())
        
        order = 0
        for item in self._config:
            
            if isinstance(item, basestring):
                # An item like 'manager'
                setattr(self, item, Role(name=item, order=order))
                order += 1
            else:
                # Anything else
                raise ImproperlyConfigured(_INCORRECT_ARGS)


roles = Roles()
