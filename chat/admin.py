from django.contrib import admin
from chat.models import Room, Chat


class RoomAdmin(admin.ModelAdmin):

    list_horizontal = ['invited_user']
    list_display = ("creator", "date")


class ChatAdmin(admin.ModelAdmin):

    list_display = ("room", "user", "text", "date")


admin.site.register(Chat, ChatAdmin)
admin.site.register(Room, RoomAdmin)
