""" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
URLS.py written for testing purpose only
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! """

from django import http
from django.conf.urls import url, include
from django.template import Template, RequestContext


def add_session(request):
    """
    Playing with the session in tests can be sometimes painful,
    This view will easily do the job.

       client.get("/set_session/", {"key": "custom_value", "val": "User2 value"})

    """
    request.session[request.GET["key"]] = request.GET["val"]
    return http.HttpResponse("ok")


def test_view(request):
    c = RequestContext(request)
    content = Template('{{ request.user.username }}').render(c)
    return http.HttpResponse(content)


urlpatterns = [
    url(r'^$', test_view),
    url(r'^set_session/$', add_session),
    url(r'^auth/', include('multiple_auth.urls')),
    url(r'^django-auth/', include('django.contrib.auth.urls')),
]
