from django.template import Template, RequestContext
from django.contrib.auth.models import User
from django.test import TestCase, Client

from django.core.urlresolvers import reverse
from django.contrib.auth import SESSION_KEY


def get_new_user(index):
    user = User(username="testuser%s" % index)
    user.set_password("test")
    user.save()
    return user


class MultipleAuthTestCase(TestCase):
    def setUp(self):
        self.user1 = get_new_user(1)
        self.user2 = get_new_user(2)
        self.login_url = reverse("multiauth_login")

    def render(self, t, request):
        return Template('{% load multiple_auth_tags %}' + t).render(RequestContext(request))

    def log_users(self):
        for u in [self.user1, self.user2]:
            response = self.client.post(self.login_url, {"username": u.username, "password": "test"}, follow=True)
        return response

    def test_get_logged_in_users(self):
        "Test the template tag"
        response = self.log_users()
        request = response.context["request"]
        datas = self.render(
            "{% get_logged_in_users as users %}{% for u in users %}{{ u.username }},{% endfor %}",
            request=request
        )
        self.assertEqual(datas, "testuser1,testuser2,")

    def test_user_session(self):
        client = Client()
        client.post(self.login_url, {"username": self.user1.username, "password": "test"})
        self.assertEqual(client.session[SESSION_KEY], str(self.user1.id)) 
        client.post(self.login_url, {"username": self.user2.username, "password": "test"})
        self.assertEqual(client.session[SESSION_KEY], str(self.user2.id)) 
        client.get(reverse("multiauth_switch", args=[0]))
        self.assertEqual(client.session[SESSION_KEY], str(self.user1.id)) 
        client.get(reverse("multiauth_switch", args=[1]))
        self.assertEqual(client.session[SESSION_KEY], str(self.user2.id)) 

    def test_user_preferences(self):
        "Test that the defined user session dictionnary is saved and restored"
        client = Client()

        # Login first user and set something in the user's session
        client.post(self.login_url, {"username": self.user1.username, "password": "test"})
        client.get("/set_session/", {"key": "custom_value", "val": "User1 value"})
        self.assertIn("custom_value", client.session)
        self.assertEqual(client.session["custom_value"], "User1 value") 
        self.assertEqual(client.session["users_preferences"], {})

        # Login second user
        client.post(self.login_url, {"username": self.user2.username, "password": "test"})
        self.assertEqual(client.session["users_preferences"], {self.user1.id: {u'custom_value': u'User1 value'}})
        self.assertNotIn("custom_value", client.session)

        # Setting something into user2's session
        client.get("/set_session/", {"key": "custom_value", "val": "User2 value"})
        self.assertEqual(client.session["users_preferences"], {self.user1.id: {u'custom_value': u'User1 value'}})
        self.assertEqual(client.session["custom_value"], "User2 value") 

        # Switching will save user2 session and restor user1 session
        client.get(reverse("multiauth_switch", args=[0]))
        self.assertEqual(client.session["custom_value"], "User1 value") 
        self.assertEqual(client.session["users_preferences"], {
            self.user1.id: {u'custom_value': u'User1 value'},
            self.user2.id: {u'custom_value': u'User2 value'}
        })

    def test_switch_unknown(self):
        self.log_users()
        response = self.client.get(reverse("multiauth_switch", args=[2]))
        self.assertEqual(response.status_code, 302)
