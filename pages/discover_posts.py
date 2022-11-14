from typing import List
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.db.models.query_utils import Q
from django.db.models import F, Count
from posts.models import Post
from posts.serializers import PostSerializer
from users.models import User
from pulsar.decorators.jwt_required import jwt_required
from users.interests import get_interests


@jwt_required()
def discover_posts(request, **kwargs):
    tag = request.GET.get("tag", "For you")
    limit = int(request.GET.get("limit", 24))
    offset = int(request.GET.get("offset", 0)) * limit

    request_user_id = kwargs.get("request_user")

    try:
        request_user = User.objects.get(id=request_user_id)
    except ObjectDoesNotExist:
        return JsonResponse(
            status=403,
            data={"message": "You are not authorized to access this endpoint"},
        )

    interests: List = get_interests(request_user)

    interests_id = list(map(lambda x: x["id"], interests))

    if tag == "Trending":
        # order by engagement, preferably not in impressions, viewed by people you share interests, interests is user's category
        print("Trending")
        posts_query = (
            Post.objects.annotate(
                engagement=Count("post_like")
                + Count("post_comment")
                + Count("post_repost")
            )
            .filter(
                Q(
                    view__user__in=User.objects.filter(
                        Q(interest__category__in=interests_id)
                        | Q(interest__category__parent__in=interests_id)
                        | Q(interest__category__subcategoryId__in=interests_id)
                    )
                )
                | Q(user__interest__category=request_user.category)
                | Q(user__interest__category__parent=request_user.category)
                | Q(user__interest__category__subcategoryId=request_user.category)
            )
            .order_by("engagement")
            .exclude(user=request_user)[offset : limit + offset]
        )
        # .distinct('id')[offset:limit+offset]
    elif tag == "For you":
        # user.category in interests, same user category, viewed by people you follow
        posts_query = (
            Post.objects.filter(
                Q(user__category__in=interests_id)
                | Q(user__category__parent__in=interests_id)
                | Q(user__category__subcategoryId__in=interests_id)
                | Q(user__category=request_user.category)
                | Q(user__category__parent=request_user.category)
                | Q(user__category__subcategoryId=request_user.category)
                | Q(
                    view__user__in=User.objects.filter(
                        followedId__follower=request_user
                    )
                )
            )
            .exclude(user=request_user)
            .distinct("id")[offset : limit + offset]
        )
    else:
        posts_query = (
            Post.objects.filter(
                Q(tag__tag__icontains=tag)
                | Q(user__category__name__iexact=tag)
                | Q(user__category__parent__name__iexact=tag)
                | Q(user__category__subcategoryId__name__iexact=tag)
                | Q(post_comment__tag__tag__icontains=tag)
            )
            .exclude(user=request_user)
            .distinct("id")[offset : limit + offset]
        )

    posts = []

    for post in posts_query:
        posts.append(
            PostSerializer(
                instance=post, context={"request_user_id": request_user_id}
            ).data
        )

    return JsonResponse(status=200, data={"posts": posts})
