from django.test import TestCase
from rest_framework.test import APIClient
from django.shortcuts import reverse
from django.contrib.auth.models import User


class TestNewUserAuth(TestCase):

    def setUp(self):
        u = 'test'
        p = 'testpass'
        user = User.objects.create(username=u)
        user.set_password(p)
        user.save()
        
        self.u = u
        self.p = p
        self.user = user

    def test_sign_in(self):
        r = self.client.post(reverse("adv_token_login"), {"username":self.u, "password":"wrong"})        
        self.assertEqual(r.status_code, 401)
        
        r = self.client.post(reverse("adv_token_login"), {"username":self.u, "password":self.p})        
        self.assertEqual(r.status_code, 200)
        assert r.json()["token"]
        token = r.json()["token"]

        self.api_client = APIClient()
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {str(token)}")

        
    def test_token(self):
        r = self.client.get(reverse("adv_token"))
        self.assertEqual(r.status_code, 401)
        self.test_sign_in()
        r = self.api_client.get(reverse("adv_token"))
        self.assertEqual(r.status_code, 200)
        
    def test_logout(self):
        self.test_sign_in()
        r = self.api_client.get(reverse("adv_token"))
        self.assertEqual(r.status_code, 200)
        r = self.api_client.get(reverse("adv_token_logout"))
        self.assertEqual(r.status_code, 200)
        r = self.api_client.get(reverse("adv_token"))
        self.assertEqual(r.status_code, 401)

    def test_change_token(self):
        self.test_sign_in()

        r = self.api_client.put(reverse("adv_token"))
        self.assertEqual(r.status_code, 200)

        new_token = r.json()["token"]

        r = self.api_client.get(reverse("adv_token"))
        self.assertEqual(r.status_code, 401)

        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {str(new_token)}")

        r = self.api_client.get(reverse("adv_token"))
        self.assertEqual(r.status_code, 200)

