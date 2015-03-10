from django.contrib.auth.decorators import user_passes_test
from userroles.models import UserRole
from userroles import roles


def role_required(*user_roles):
    """
    Decorator for views that checks whether a user has a particular role,
    redirecting to the log-in page if neccesary.
    Follows same style as django.contrib.auth.decorators.login_required,
    and django.contrib.auth.decorators.permission_required.
    """    
    required_roles = []
    for each in user_roles:
        if isinstance(each, basestring):
            required_roles.append( roles.get(each) )
        else:
            required_roles.append(each)
    
    def check_role(user):
        try:
            user_role = getattr(user, 'role', None)
            if not user_role:
                return False
            for each in required_roles:
                if user_role == each or user_role.subrole_of( each ):
                    return True
            return False
            # return getattr(user, 'role', None) in required_roles
        except UserRole.DoesNotExist:
            return False
    return user_passes_test(check_role)
