from rest_framework import serializers

from django.contrib.auth.models import User
from chat.models import Room, Chat


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username")


class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('creator', 'invited_user', 'date')


class ChatSerializers(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Chat
        fields = ("user", "text", "date")


class ChatSerializers(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Chat
        fields = ("user", "text", "date")


class ChatPostSerializers(serializers.ModelSerializer):


    class Meta:
        model = Chat
        fields = ("room", "text")