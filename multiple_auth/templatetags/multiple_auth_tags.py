from django import template
from django.contrib.auth import get_user_model

from multiple_auth import SESSION_KEY, LOGGED_USERS_KEY


register = template.Library()


@register.simple_tag(takes_context=True)
def get_logged_in_users(context):
    users_id = [int(data[SESSION_KEY]) for data in context["request"].session.get(LOGGED_USERS_KEY, [])]
    User = get_user_model()
    users = User.objects.filter(id__in=users_id)

    # Small trick to keep initial ids ordering
    users = dict([(user.id, user) for user in users])
    return [users[pk] for pk in users_id]