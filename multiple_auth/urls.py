from django.conf.urls import url
from .views import login, switch


urlpatterns = [
    url(r'^login/$', login, name='multiauth_login'),
    url(r'^u/(?P<user_index>\d+)/$', switch, name='multiauth_switch'),
]
