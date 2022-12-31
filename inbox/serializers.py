from rest_framework import serializers
from .models import ChatMaster, ChatMessage

class ChatMasterSErializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMaster
        fields = "__all__"


class ChatMessageSErializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMessage
        fields = "__all__"



# class MentorSErializer(serializers.ModelSerializer):
#     username = serializers.SerializerMethodField()

#     def get_username(self, instance):
#         return instance.mentor.username if instance.gigger else ""

#     class Meta:
#         model = Mentors
#         fields = "__all__"