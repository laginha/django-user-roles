from django.conf import settings
from django.db import models
from userroles import roles


class UserRole(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='role')
    name = models.CharField(max_length=100, choices=roles.choices)
    child = models.CharField(max_length=100, blank=True)
    _valid_roles = roles

    @property
    def profile(self):
        if not self.child:
            return None
        return getattr(self, self.child)

    def __eq__(self, other):
        return self.name == other.name

    def __getattr__(self, name):
        if name.startswith('is_'):
            role = getattr(self._valid_roles, name[3:], None)
            if role:
                return self == role or self.subrole_of( role )
        role = roles.get(self.name)
        if hasattr(role, name):
            return getattr(role, name)
        raise AttributeError("'%s' object has no attribute '%s'" %
                              (self.__class__.__name__, name))

    def __unicode__(self):
        return self.name


def set_user_role(user, role):
    role_name = role if isinstance(role, basestring) else role.name
    try:
        profile = UserRole.objects.get(user=user)
    except UserRole.DoesNotExist:
        profile = UserRole(user=user, name=role_name)
    else:
        profile.name = role_name
    profile.save()

