from rest_framework import serializers
from .models import University, Mentors, Comments, FavMentor


class UniversitySErializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"


class MentorSErializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    uni = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    # universities = serializers.CharField(source='universities.name', read_only=True)

    def get_username(self, instance):
        return instance.mentor.username if instance.mentor else ''

    def get_uni(self, istance):
        uni = istance.universities.first()
        return uni.name if istance.universities else ''

    def get_profile_pic(self, instance):
        return instance.mentor.profile_pic.url if instance.mentor else ''

    class Meta:
        model = Mentors
        fields = "__all__"

class CommentsSerializer(serializers.ModelSerializer):
    # author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comments
        fields = "__all__"

class FavMentorSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavMentor
        fields = "__all__"
