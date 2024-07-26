from rest_framework import serializers
from .models import Room, Message


# Сериализатор для модели Message
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'content', 'timestamp']

# Сериализатор для модели  Room
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name']
