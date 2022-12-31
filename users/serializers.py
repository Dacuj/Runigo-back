from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Group, Permission

from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    group_name = serializers.SerializerMethodField()
    group_permission = serializers.SerializerMethodField()
   

    def get_group_name(self, instance):
        return ((g.name) for g in instance.groups.all() )if instance.groups else ''
        # return instance.groups.values_list('name',flat = True) if instance.groups else ''

    def get_group_permission(self, instance):
        return instance.groups.values_list('permissions__name',flat = True) if instance.groups else ''

    
    # def get_username(self, instance):
    #     return instance.mentor.username if instance.mentor else ''

    class Meta:
        model = User
        # exclude = ('password', )
        fields = '__all__'


class LoggedInUserDetailSerializer(ModelSerializer):
    group_name = serializers.SerializerMethodField()
    def get_group_name(self, instance):
        return ((g.name) for g in instance.groups.all() )if instance.groups else ''
    class Meta:
        model = User
        exclude = ('password', )
        # fields = '__all__'
         

# class UserViewSet()

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "is_mentor")
        # exclude = ['password']
        # read_only_fields = ('last_login', 'date_joined', 'groups', "email", "userfrom")


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'
        # read_only_fields = ('name',)



class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    username = serializers.CharField(required=True, write_only=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': 'Pass@123',
            # 'password1':  BaseUserManager.make_random_password(self, length=10,
            # allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        #    self.custom_signup(request, user)
        setup_user_email(request, user, [])
        user.save()
        # new_user_register.delay('company_name',self.cleaned_data['email'],self.cleaned_data['password1'])

        #        try:
        #            html_message = loader.render_to_string(
        #                'email-registration.html',
        #                {
        #                    'subject':  'Welcome email from app Name',
        #                    'company_name' : 'company_name',
        #                    'username' : self.cleaned_data['email'],
        #                    'password' : self.cleaned_data['password1']
        #                }
        #            )
        #            send_mail(
        #            'Welcome to Works.Fashion',
        #            'Here',
        #            'admin@example.com',
        #            [self.cleaned_data['email']],
        #            fail_silently=False,
        #            html_message=html_message
        #            )
        #        except:
        #            pass
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ('changed_password', 'last_login', 'date_joined', "email", "tenant")

    # def update(self, instance, validated_data):
    #     # We try to get profile data
    #     profile_data = validated_data.pop('profile', None)
    #     # If we have one
    #     if profile_data is not None:
    #         # We set address, assuming that you always set address
    #         # if you provide profile
    #         instance.profile.profile_pic = profile_data['img_url']
    #         # And save profile
    #         instance.profile.save()
    #     # Rest will be handled by DRF
    #     return super().update(instance, validated_data)
