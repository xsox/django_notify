from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "telegram_chat_id")
    search_fields = ("user__username", "user__email", "phone_number", "telegram_chat_id")
    list_filter = ()
