from typing import List
from django.core.exceptions import ObjectDoesNotExist
from users.models import Interest

from users.category import Category


def save_interests(user, interests):

    # Delete existing interests
    if interests != "":
        Interest.objects.filter(user=user).delete()
    interests_list: List = interests.split(",")
    for interest in interests_list:
        try:
            category = Category.objects.get(name__iexact=interest)
        except ObjectDoesNotExist:
            pass
        else:
            interest = Interest(category=category, user=user)
            interest.save()


def get_interests(user) -> list:
    interests = []
    interests_query = Category.objects.filter(interest__user=user).values()
    interests = list(interests_query)
    return interests
