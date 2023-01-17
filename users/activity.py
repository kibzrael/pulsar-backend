import enum
from users.models import User
from posts.models import Post, Comment
from django.utils import timezone

from firebase_admin import firestore
from firebase_admin.firestore import firestore as fr
from media.cert import firebase_initialization


class Activity(enum.Enum):
    follow = 1
    like = 2
    comment = 3
    repost = 4
    notification = 5


def activity(
    receipient: User,
    activity_type: Activity,
    user: User = None,
    post: Post = None,
    comment: Comment = None,
):
    media = None
    description = ""
    if comment:
        user = comment.user
        media = comment.post.thumbnail.thumbnail
        description = f"Commented your post: {comment.comment}"
    elif post:
        media = post.thumbnail.thumbnail

    if activity_type == Activity.like:
        description = f"Liked your post"
    elif activity_type == Activity.repost:
        description = f"Reposted your post"
    elif activity_type == Activity.follow:
        description = f"Followed you"

    data = {
        "userId": user.id,
        "thumbnail": user.profile_pic.thumbnail,
        "username": user.username,
        "time": timezone.now(),
        "description": description,
        "media": media,
        "link": "",
        "type": activity_type.name,
    }

    firebase_initialization()
    db = firestore.client()
    col_ref: fr.CollectionReference = (
        db.collection("users").document(str(receipient.id)).collection("activities")
    )
    col_ref.add(data)
