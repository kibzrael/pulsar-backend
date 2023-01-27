import enum
from authentication.models import User
from pulsar.decorators.jwt_required import jwt_required
from users.models import Activity, Device
from posts.models import Post, Comment
from django.http.response import JsonResponse

from firebase_admin import firestore, messaging
from firebase_admin.firestore import firestore as fr
from media.cert import firebase_initialization
from users.serializers import ActivitySerializer


class ActivityType(enum.Enum):
    follow = 1
    like = 2
    comment = 3
    repost = 4
    notification = 5


@jwt_required()
def fetch_activity(request, **kwargs):
    request_user_id = kwargs.get("request_user")
    limit = int(request.GET.get("limit", 20))
    offset = int(request.GET.get("offset", 0)) * limit

    query = Activity.objects.filter(receipient__id=request_user_id).order_by("-time")[
        offset : limit + offset
    ]
    data = []
    for result in query:
        data.append(
            ActivitySerializer(
                instance=result, context={"request_user_id": request_user_id}
            ).data
        )
    return JsonResponse(data={"activity": data})


def activity(
    receipient: User,
    activity_type: ActivityType,
    user: User = None,
    post: Post = None,
    comment: Comment = None,
):
    media = None
    description = ""
    if comment:
        user = comment.user
        media = comment.post.thumbnail
        description = f"Commented your post: {comment.comment}"
    elif post:
        media = post.thumbnail

    if activity_type == ActivityType.like:
        description = f"Liked your post"
    elif activity_type == ActivityType.repost:
        description = f"Reposted your post"
    elif activity_type == ActivityType.follow:
        description = f"Followed you"
    elif activity_type == ActivityType.notification:
        description = f"Shared a video"

    activity_obj = Activity(
        receipient=receipient,
        user=user,
        media=media,
        description=description,
        link="",
        type=activity_type.name,
    )
    activity_obj.save()

    data = ActivitySerializer(
        instance=activity_obj, context={"request_user_id": receipient.id}
    ).data
    print(data)

    firebase_initialization()
    db = firestore.client()
    col_ref: fr.CollectionReference = (
        db.collection("users").document(str(receipient.id)).collection("activities")
    )
    col_ref.add(data)

    device = Device.objects.filter(user__id=receipient.id).last()

    if device:
        print("Device Found")
        message = messaging.Message(
            notification=messaging.Notification(
                title=f"@{data['user']['username']}",
                body=description,
                image=media.high,
            ),
            android=messaging.AndroidConfig(
                notification=messaging.AndroidNotification(
                    icon=user.profile_pic.thumbnail
                )
            ),
            token=device.token,
        )
        response = messaging.send(message)
        print(f"Successfully sent: {response}")
