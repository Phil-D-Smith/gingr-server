from django.contrib import admin

from .models import UserProfile, Decision, Match, Message

# include databases on admin site for editing
admin.site.register(UserProfile)
admin.site.register(Decision)
admin.site.register(Match)
admin.site.register(Message)