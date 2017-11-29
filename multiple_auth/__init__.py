from django.middleware.csrf import rotate_token
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import _get_backends
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY

LOGGED_USERS_KEY = "logged_in_users"
USERS_PREFERENCES_KEY = "users_preferences"


def store_user_preferences(request):
    # Keys in the session that won't be altered
    if not request.user.is_authenticated:
        request.session[USERS_PREFERENCES_KEY] = {}
    else:
        dont_store_keys = [
            SESSION_KEY, BACKEND_SESSION_KEY, 
            HASH_SESSION_KEY, USERS_PREFERENCES_KEY, LOGGED_USERS_KEY
        ]
        # Entire session dict without the Django-Reserved keys above
        user_preferences = dict([(k, request.session.pop(k)) for k in dict(request.session).iterkeys() if k not in dont_store_keys])
        request.session.setdefault(USERS_PREFERENCES_KEY, {})[request.user.id] = user_preferences


def xlogin(request, user, backend=None):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    """
    session_auth_hash = ''
    if user is None:
        user = request.user
    if hasattr(user, 'get_session_auth_hash'):
        session_auth_hash = user.get_session_auth_hash()

    # Hack to init the session
    request.session._get_session()

    request.session.cycle_key()
    try:
        backend = backend or user.backend
    except AttributeError:
        backends = _get_backends(return_tuples=True)
        if len(backends) == 1:
            _, backend = backends[0]
        else:
            raise ValueError(
                'You have multiple authentication backends configured and '
                'therefore must provide the `backend` argument or set the '
                '`backend` attribute on the user.'
            )

    logged_in_user = {
        SESSION_KEY: user._meta.pk.value_to_string(user),
        BACKEND_SESSION_KEY: backend,
        HASH_SESSION_KEY: session_auth_hash
    }

    request.session.setdefault(LOGGED_USERS_KEY, []).append(logged_in_user)
    request.session.update(logged_in_user)
    if hasattr(request, 'user'):
        request.user = user
    rotate_token(request)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
