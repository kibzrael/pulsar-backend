from django.contrib import admin

from challenges.models import Challenge, ChallengeImpression, Pin

# Register your models here.
admin.site.register(Challenge)
admin.site.register(ChallengeImpression)
admin.site.register(Pin)
