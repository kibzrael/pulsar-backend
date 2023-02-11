from django.contrib import admin

from posts.models import (
    Post,
    PostImpression,
    Like,
    Mention,
    Comment,
    CommentLike,
    Repost,
    View,
    Tag,
)

# Register your models here.
admin.site.register(Post)
admin.site.register(PostImpression)
admin.site.register(Like)
admin.site.register(Mention)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Repost)
admin.site.register(View)
admin.site.register(Tag)
