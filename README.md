Django Multiple Auth
====================

django-multiple-auth allows you to login over a Django website with
many users and quickly switch without having to type credentials.


[![Build Status](https://travis-ci.org/EngageSports/django-multiple-auth.svg?branch=master)](https://travis-ci.org/EngageSports/django-multiple-auth)


Requirements
------------

 - Django 1.10.* / Django 1.11.*
 - Tested under python 2.7 and 3.6


Install
-------

```
pip install django-multiple-auth
```


Add `multiple_auth` to INSTALLED_APPS

```python
INSTALLED_APPS = (
    ...
    'multiple_auth',
)
```

then update your project's `urls.py`:

```python
urlpatterns = patterns(
    ...
    url(r'^m_auth/', include('multiple_auth.urls')),
)
```

Usage
-----

Replace the usage of `django.contrib.auth.views.login` by `multiple_auth.views.login`
    
```python
from multiple_auth.views import login

urlpatterns = patterns(
   url(r'^login/$', login, name='auth_login'),
]
```

This view must be used to login new users, including the first login. 


In your template, load the template tag, show a list of logged-in users and give access to the login form.

```html
{% load multiple_auth_tags %}

{% block content %}
    {% get_logged_in_users as logged_in_users %}
    <ul>
        {% for u in logged_in_users %}
            <li>
                {% if u != request.user %}
                    <b>{{ u.username }}</b> - {{ u.get_full_name }}
                {% else %}
                    <a href="{% url "multiauth_switch" forloop.counter0 %}">
                        <b>{{ u.username }}</b> - {{ u.get_full_name }}
                    </a>
                {% endif %}
            </li>
        {% endfor %}
    </ul>
    <a href="{% url "multiauth_login" %}">Add account</a>
{% endblock content %}
```


