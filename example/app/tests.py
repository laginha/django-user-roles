from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from django.contrib.auth.models import User
from userroles.models import set_user_role
from userroles import roles, Role


class UserRolesTest(TestCase):
    
    def create_user(self, username):
        return User.objects.create_user(username, username, username)
    
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
        user = self.create_user('username')
        set_user_role(user, role_name)
        self.assertTrue( user.role == roles.get(role_name) )
        self.assertTrue( getattr(user.role, 'is_'+role_name) )
        for each in getattr( settings, 'USER_ROLES' )[1:]:
            self.assertFalse( user.role == roles.get(each) )
            self.assertFalse( getattr(user.role, 'is_'+each) )
    
    def test_set_subrole(self):
        for role_name in getattr( settings, 'USER_ROLES' ):
            for subrole_name in getattr( settings, role_name.upper()+'_ROLES', () ):
                user = self.create_user( subrole_name )
                set_user_role(user, subrole_name)
                self.assertTrue( user.role == roles.get(subrole_name) )
                self.assertTrue( getattr(user.role, 'is_'+subrole_name) )
                self.assertTrue( getattr(user.role, 'is_'+role_name) )
            user = self.create_user( role_name )
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
            
    def test_role_required(self):
        def assert_it(name, status):
            user = self.create_user( name )
            set_user_role(user, name)
            client = Client()
            client.login(username=name, password=name)
            self.assertEqual( client.get('/').status_code, status )
        
        required_role = 'manager'
        for each in getattr( settings, required_role.upper()+'_ROLES', () ):   
            assert_it( each, status=200 )
        for each in getattr( settings, 'USER_ROLES' ):
            assert_it( each, status= 200 if each==required_role else 302 )
