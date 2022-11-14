from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from posts.models import Post, Comment, CommentLike
from posts.serializers import CommentSerializer
from users.models import User
from users.serializers import MinimalUserSerializer

from pulsar.decorators.jwt_required import jwt_required
from posts.create_post import save_hashtags


@method_decorator(csrf_exempt, name="dispatch")
class CommentsView(View):
    # get comments of a certain post
    @jwt_required()
    def get(self, request, post_id, **kwargs):
        limit = int(request.GET.get("limit", 18))
        offset = int(request.GET.get("offset", 0)) * limit

        reply_to = request.GET.get("replyTo")
        reply_to_comment = None

        if reply_to:
            try:
                reply_to_comment = Comment.objects.get(id=int(reply_to))
            except ObjectDoesNotExist:
                return JsonResponse(
                    status=404,
                    data={"message": "The comment you've entered does not exist."},
                )

        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "The post you've entered does not exist."}
            )

        comments_query = Comment.objects.filter(post=post, reply_to=reply_to_comment)[
            offset : limit + offset
        ]
        comments = []
        for comment in comments_query:
            comments.append(
                CommentSerializer(
                    instance=comment,
                    context={"request_user_id": kwargs.get("request_user")},
                ).data
            )
        return JsonResponse(status=200, data={"comments": comments})

    # comment on a certain post
    @jwt_required()
    def post(self, request, post_id, **kwargs):
        request_user = kwargs.get("request_user")
        comment = request.POST.get("comment")
        reply_to = request.POST.get("replyTo")
        reply_to_comment = None

        if not comment:
            return JsonResponse(status=422, data={"message": "Please enter a comment"})

        try:
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=request_user)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "The post you've entered does not exist."}
            )

        if reply_to:
            try:
                reply_to_comment = Comment.objects.get(id=int(reply_to))
            except ObjectDoesNotExist:
                return JsonResponse(
                    status=404,
                    data={"message": "The comment you've entered does not exist."},
                )

        comment_object = Comment(
            user=user, post=post, comment=comment, reply_to=reply_to_comment
        )
        comment_object.save()

        save_hashtags(post=post, caption=comment, comment=comment_object)
        comment_info = CommentSerializer(
            instance=comment_object, context={"request_user_id": request_user}
        ).data
        return JsonResponse(status=200, data={"comment": comment_info})


@method_decorator(csrf_exempt, name="dispatch")
class CommentView(View):
    # delete a certian comment
    @jwt_required()
    def delete(self, request, comment_id, **kwargs):
        request_user_id = kwargs.get("request_user")

        try:
            comment = Comment.objects.get(id=comment_id)

            if comment.user.id != request_user_id:
                return JsonResponse(
                    status=403,
                    data={"message": "You are not authorized to access this endpoint"},
                )
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The comment you've entered does not exist."},
            )

        comment.delete()

        return JsonResponse(
            status=200, data={"message": "You have successfully deleted this comment"}
        )


#
#
@method_decorator(csrf_exempt, name="dispatch")
class CommentLikeView(View):
    # get likes of a certain comment
    @jwt_required()
    def get(self, request, comment_id, **kwargs):
        limit = int(request.GET.get("limit", 18))
        offset = int(request.GET.get("offset", 0)) * limit

        try:
            comment = Comment.objects.get(id=comment_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The comment you've entered does not exist."},
            )

        likes_query = User.objects.filter(comment_liker__comment__id=comment_id)[
            offset : limit + offset
        ]
        likes = []
        for like in likes_query:
            likes.append(
                MinimalUserSerializer(instance=like).data,
                context={"request_user_id": kwargs.get("request_user")},
            )
        return JsonResponse(status=200, data={"likes": likes})

    # like a certain comment
    @jwt_required()
    def post(self, request, comment_id, **kwargs):
        request_user_id = kwargs.get("request_user")

        try:
            comment = Comment.objects.get(id=comment_id)
            user = User.objects.get(id=request_user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The comment you've entered does not exist."},
            )

        try:
            CommentLike.objects.filter(user=user, comment=comment).get()
        except ObjectDoesNotExist:
            like = CommentLike(user=user, comment=comment)
            like.save()

            return JsonResponse(
                status=200, data={"message": "You have successfully liked the comment"}
            )
        else:
            return JsonResponse(
                status=200, data={"message": "You have already liked the comment"}
            )

    # unlike a certain comment
    @jwt_required()
    def delete(self, request, comment_id, **kwargs):
        request_user_id = kwargs.get("request_user")

        try:
            comment = Comment.objects.get(id=comment_id)
            user = User.objects.get(id=request_user_id)

        except ObjectDoesNotExist:
            return JsonResponse(
                status=404,
                data={"message": "The comment you've entered does not exist."},
            )

        try:
            like = CommentLike.objects.filter(user=user, comment=comment).get()
            if (
                like.user.id != request_user_id
                or comment.post.user.id != request_user_id
            ):
                return JsonResponse(
                    status=403,
                    data={"message": "You are not authorized to access this endpoint"},
                )
            like.delete()
        except ObjectDoesNotExist:
            return JsonResponse(
                status=404, data={"message": "You have not liked this comment"}
            )

        return JsonResponse(
            status=200, data={"message": "You have successfully unliked this comment"}
        )


#
#
