Django User Roles
=================

Simple role-based user permissions for Django.

django-user-roles is a simple, reusable app that allows you to create a set of user roles, which can be used to control which views each type of user has permission to view, and to customize how the site is presented to different types of user.

<!--
User roles can also be associated with differing profile classes, allowing you to store different types of user information for different user types.
-->

## Install

    pip install git+https://github.com/laginha/django-user-roles


## Usage

Add `userroles` do `INSTALLED_APPS`

```python
INSTALLED_APPS = (
    ...
    'userroles',
)
```

and add the `USER_ROLES` setting to your `settings.py`. For example:

```python
USER_ROLES = (
    'manager',
    'moderator',
    'client',
)
```

### Sub-roles

Add sub-roles for any of the roles defined in the `USER_ROLES` setting.

```python
MANAGER_ROLES = (
    'staff_manager', 'bussiness_manager'
)
```

Be careful not to repeat the names in subroles and roles.

#### subrole_of

```python
from userroles import roles

roles.staff_manager.subrole_of( 'manager' ) == True
roles.staff_manager.subrole_of( roles.manager ) == True

roles.staff_manager.subrole_of( 'moderator' ) == False
roles.staff_manager.subrole_of( roles.moderator ) == False

```

#### has_subrole

```python
from userroles import roles

roles.manager.has_subrole( 'staff_manager' ) == True
roles.manager.has_subrole( roles.staff_manager ) == True

roles.moderator.has_subrole( 'staff_manager' ) == False
roles.moderator.has_subrole( roles.staff_manager ) == False
```


### Get (sub)role

```python
from userroles import roles

roles.manager
roles.get('manager')
```

### Set (sub)role

```python
from userroles.models import set_user_role

set_user_role(self.user, 'manager')
```

or

```python
from userroles.models import set_user_role
from userroles import roles

set_user_role(self.user, roles.manager)
```

### Check (sub)role

```python
from userroles import roles

user.role == roles.manager
user.role in (roles.manager, roles.moderator)
user.role.is_moderator
user.role.is_staff_manager
```


## Decorator

The `role_required` decorator provides similar behavior to Django's `login_required` and `permission_required` decorators.  If the user accessing the view does not have the required roles, they will be redirected to the login page.

```python
from userroles.decorators import role_required

@role_required('manager', 'moderator')
def view(request):
    ...
```

or

```python
from userroles.decorators import role_required
from userroles import roles

@role_required(roles.manager, roles.moderator)
def view(request):
    ...
```

If user has a subrole of the required role, it passes de user test as well!
