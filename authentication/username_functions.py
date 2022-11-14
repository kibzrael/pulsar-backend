from django.core.exceptions import ObjectDoesNotExist
from users.models import User


allowed_characters = "abcdefghijklmnopqrstuvwxyz1234567890 ._"


def validate_username(username):
    # check for appropriate length
    if not 1 <= len(username) <= 15:
        return False
    for i in username:
        if i not in allowed_characters and i.lower() not in allowed_characters:
            return False
    return True


def not_username_exists(username):
    try:
        User.objects.get_by_natural_key(username)
    except ObjectDoesNotExist:
        return True
    else:
        return False
