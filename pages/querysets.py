from typing import Dict, List

from django.db.models.query_utils import Q
from django.db.models import Count, Exists, OuterRef
from users.models import User
from challenges.models import Challenge, Pin
from challenges.serializers import ChallengeSerializer
from users.interests import get_interests


def pinned_challenges(user: User, offset: int = 0, limit: int = 12) -> List:
    challenges_query = (
        Challenge.objects.annotate(
            is_pinned=Exists(Pin.objects.filter(challenge=OuterRef("id"), user=user))
        )
        .filter(Q(pin__user=user) | Q(category=user.category))
        .order_by("-is_pinned")[offset : offset + limit]
    )
    challenges = []
    for challenge in challenges_query:
        if not any(x.get("id") == challenge.id for x in challenges):
            challenges.append(
                ChallengeSerializer(
                    challenge, context={"request_user_id": user.id}
                ).data
            )
    return challenges


# order by engagement NB: Can be static, sort of a chart
def top_challenges(user: User) -> List:
    challenges_query = (
        Challenge.objects.annotate(engagement=Count("post") + Count("pin"))
        .filter()
        .order_by("-engagement")[:3]
    )
    challenges = []
    for challenge in challenges_query:
        challenges.append(
            ChallengeSerializer(challenge, context={"request_user_id": user.id}).data
        )
    return challenges


# order by time, category in user interests, preferably not in impressions
def new_challenge_highlight(user: User) -> Dict:
    challenge = (
        Challenge.objects.filter(
            # category=user.category
        )
        .order_by("-time_created")
        .first()
    )
    return ChallengeSerializer(challenge, context={"request_user_id": user.id}).data


def discover_challenges(user: User, tag: str, offset: int = 0, limit: int = 12) -> List:
    interests: List = get_interests(user)

    interests_id = list(map(lambda x: x["id"], interests))

    if tag == "Trending":
        # order by engagement, preferably not in impressions, joined by people you share interests
        challenges_query = (
            Challenge.objects.annotate(engagement=Count("post") + Count("pin"))
            .filter(
                Q(post__user__interest__category__in=interests_id)
                | Q(post__user__interest__category__parent__in=interests_id)
                | Q(post__user__interest__category__subcategoryId__in=interests_id)
            )
            .order_by("-engagement")[offset : offset + limit]
        )
        # .distinct('id')
    elif tag == "For you":
        # category is user's category or in user interests, people you're following joined
        challenges_query = Challenge.objects.filter(
            Q(category=user.category)
            | Q(category__parent=user.category)
            | Q(category__subcategoryId=user.category)
            | Q(category__in=interests_id)
            | Q(category__parent__in=interests_id)
            | Q(category__subcategoryId__in=interests_id)
            | Q(post__user__followedId__follower=user)
        ).distinct("id")[offset : offset + limit]
    else:
        challenges_query = Challenge.objects.filter(
            Q(post__tag__tag__icontains=tag)
            | Q(category__name__iexact=tag)
            | Q(category__parent__name__iexact=tag)
            | Q(category__subcategoryId__name__iexact=tag)
            | Q(post__post_comment__tag__tag__icontains=tag)
        ).distinct("id")[offset : offset + limit]
    challenges = []
    for challenge in challenges_query:
        challenges.append(
            ChallengeSerializer(challenge, context={"request_user_id": user.id}).data
        )
    return challenges
