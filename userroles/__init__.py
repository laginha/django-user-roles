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
    
    def add_subrole(self, role):
        self.subroles[ role.name ] = role
    
    def subrole_of(self, role):
        if isinstance(role, basestring):
            return bool(self.parent) and self.parent.name == role
        return bool(self.parent) and self.parent.name == role.name
    
    def has_subrole(self, role):
        if isinstance(role, basestring):
            return role in self.subroles
        return role.name in self.subroles

    def __init__(self, name, parent=None):
        self.name = name
        self.subroles = {}
        self.parent = parent

    def __unicode__(self):
        return self.name


class Roles(object):

    def get(self, userrole, *args):
        return getattr(self, userrole, *args)
    
    def add(self, name, parent=None):
        role = Role(name=name, parent=parent)
        setattr(self, name, role)
        self.choices.append( (name, name) )
        return role
    
    def __init__(self, config=None):
        """
        By default the Roles object will be created using configuration from
        the django settings file, but you can also set the configuration
        explicitly, for example, when testing.
        """
        self._config = config or getattr(settings, 'USER_ROLES', ())
        # a list of two-tuples of role names, suitable for use as the
        # 'choices' argument to a model field.
        self.choices = []
        
        def get_subroles(parent):
            subroles = getattr(settings, parent.name.upper()+'_ROLES', ())
            for each in subroles:
                role = self.add( each, parent=parent )
                parent.add_subrole( role )
                get_subroles( role )
        
        for item in self._config:
            if isinstance(item, basestring):
                # An item like 'manager'
                get_subroles( self.add( item ) )
            else:
                # Anything else
                raise ImproperlyConfigured(_INCORRECT_ARGS)


roles = Roles()
