from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.client import Client
from milkman.dairy import milkman
from userroles.models import set_user_role, UserRole
from userroles.utils import SettingsTestCase
from userroles import roles, Roles, Role

User = get_user_model()


class UserRoleTests(TestCase):
    """
    Test basic user.role operations.
    """

    def setUp(self):
        super(UserRoleTests, self).setUp()
        self.user = self.create_user()
        set_user_role(self.user, roles.manager)

    def create_user(self):
        return milkman.deliver(User)

    def test_role_comparison(self):
        """
        Ensure that we can test if a user role has a given value.
        """
        self.assertEquals(self.user.role, roles.manager)

    def test_role_in_set(self):
        """
        Ensure that we can test if a user role exists in a given set.
        """
        self.assertIn(self.user.role, (roles.manager,))

    def test_is_role(self):
        """
        Test `user.role.is_something` style.
        """
        self.assertTrue(self.user.role.is_manager)

    def test_is_not_role(self):
        """
        Test `user.role.is_not_something` style.
        """
        self.assertFalse(self.user.role.is_moderator)

    def test_is_invalid_role(self):
        """
        Test `user.role.is_invalid` raises an AttributeError.
        """
        self.assertRaises(AttributeError, getattr, self.user.role, 'is_foobar')
    
    def test_choices(self):
        choices = [each[0] for each in roles.choices]
        for role in getattr( settings, 'USER_ROLES' ):
            for subrole in getattr( settings, role.upper()+'_ROLES', () ):
                self.assertTrue( subrole in choices )
            self.assertTrue( role in choices )
    
    def test_get_roles(self):
        for each in getattr(settings, 'USER_ROLES', ()):
            self.assertTrue( roles.get(each) == getattr(roles, each) )
            self.assertTrue( isinstance(roles.get(each), Role) )
            
    def test_set_role(self):
        role_name = getattr( settings, 'USER_ROLES' )[0]
        user = self.create_user()
        set_user_role(user, role_name)
        self.assertTrue( user.role == roles.get(role_name) )
        self.assertTrue( getattr(user.role, 'is_'+role_name) )
        for each in getattr( settings, 'USER_ROLES' )[1:]:
            self.assertFalse( user.role == roles.get(each) )
            self.assertFalse( getattr(user.role, 'is_'+each) )
    
    def test_set_subrole(self):
        for role_name in getattr( settings, 'USER_ROLES' ):
            for subrole_name in getattr( settings, role_name.upper()+'_ROLES', () ):
                user = self.create_user()
                set_user_role(user, subrole_name)
                self.assertTrue( user.role == roles.get(subrole_name) )
                self.assertTrue( getattr(user.role, 'is_'+subrole_name) )
                self.assertTrue( getattr(user.role, 'is_'+role_name) )
            user = self.create_user()
            set_user_role(user, role_name)
            self.assertTrue( user.role == roles.get(role_name) )
            self.assertTrue( getattr(user.role, 'is_'+role_name) )
            self.assertFalse( getattr(user.role, 'is_'+subrole_name) )
        
    def test_subroles(self):
        for each in getattr( settings, 'USER_ROLES' ):
            role     = each
            subroles = getattr( settings, each.upper()+'_ROLES', () )
            for subrole in subroles:
                self.assertTrue( getattr(roles, subrole).subrole_of(role) )
                self.assertFalse( getattr(roles, subrole).subrole_of('some_user_role') )
                self.assertFalse( getattr(roles, role).subrole_of(subrole) )
                self.assertFalse( getattr(roles, subrole).has_subrole(role) )
                self.assertFalse( getattr(roles, subrole).has_subrole('some_user_role') )
                self.assertTrue( getattr(roles, role).has_subrole(subrole) )
            self.assertFalse( getattr(roles, role).subrole_of('some_user_role') )
            self.assertFalse( getattr(roles, role).has_subrole('some_user_role') )
            
