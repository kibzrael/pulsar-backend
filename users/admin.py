from django.contrib import admin

from users.models import (
    Category,
    Device,
    Interest,
    Follow,
    Block,
    PostNotification,
    Activity,
)

# Register your models here.
admin.site.register(Category)
admin.site.register(Device)
admin.site.register(Interest)
admin.site.register(Follow)
admin.site.register(Block)
admin.site.register(PostNotification)
admin.site.register(Activity)
