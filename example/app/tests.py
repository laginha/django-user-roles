from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from django.contrib.auth import get_user_model
from userroles.models import set_user_role
from userroles import roles, Role
from milkman.dairy import milkman

User = get_user_model()


class ViewTests(TestCase):
    def setUp(self):
        password = 'password'
        self.user = self.create_user(password)
        self.client = self.create_client(self.user.username, password)

    def create_user(self, password):
        user = milkman.deliver(User)
        user.set_password(password)
        user.save()
        return user

    def create_client(self, username, password):
        client = Client()
        client.login(username=username, password=password)
        return client

    def test_get_allowed_view(self):
        set_user_role(self.user, roles.manager)
        resp = self.client.get('/manager_or_moderator/')
        self.assertEquals(resp.status_code, 200)

    def test_get_disallowed_view(self):
        set_user_role(self.user, roles.client)
        resp = self.client.get('/manager_or_moderator/')
        self.assertEquals(resp.status_code, 302)
        
    def test_role_required(self):
        def assert_it(name, status):
            user = self.create_user(password=name)
            set_user_role(user, name)
            client = self.create_client(user.username, name)
            self.assertEqual( client.get('/manager/').status_code, status )

        required_role = 'manager'
        for each in getattr( settings, required_role.upper()+'_ROLES', () ):
            assert_it( each, status=200 )
        for each in getattr( settings, 'USER_ROLES' ):
            assert_it( each, status= 200 if each==required_role else 302 )
    
