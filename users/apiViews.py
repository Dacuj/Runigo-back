from rest_framework.viewsets import ModelViewSet
from .serializers import UserDetailSerializer, LoggedInUserDetailSerializer, UserSerializer, PermissionSerializer, GroupSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response


from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser
from rest_framework import viewsets
from chatapp.permission import DjangoModelPermissionsWithRead
from rest_framework.decorators import action




from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import PasswordChangeView

from rest_framework import status

from rest_framework import generics

# for token last login
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserUpdateSerializer
from rest_framework.views import APIView



#image field 
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth import get_user_model

User = get_user_model()





class UserDetailViewset(ModelViewSet):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithRead]

    def list(self, request):
        clientId = request.GET.get('client', None)
        print("clientId")
        print(clientId)
        # print(recievedItemName)
        # brancheList = BranchInSameTenant(self, self.request.user.id)
        # print(brancheList)
        if clientId is not None:
            queryset = User.objects.filter(client=clientId)
        else:
            queryset = User.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        # user = request.GET.get("user")
        # print(user)
        # if user is not None:
        #     print(user)
        #     queryset = User.objects.filter(username=user)
        # else:
        #     queryset = User.objects.all()
            
                    # serializer = (data=request.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)   


    @action(detail=True, methods=["put"])
    def UploadImages(self, request, pk=None):
        user = self.get_object()
        serializer = UserDetailSerializer(profile_pic=request.data['file'])
        if serializer.is_valid():
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    # def perform_update(self, request, serializer):
    #     file = request.data['file']
    #     serializer(profile_)
            



class UserDetail(ListAPIView):
    # queryset = User.objects.all()
    serializer_class = LoggedInUserDetailSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithRead]

    def get_queryset(self):
        # print(request.user.id)
        queryset = User.objects.filter(id=self.request.user.id)
        # serializer = LoggedInUserDetailSerializer(queryset, many=True)
        return queryset

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [IsAuthenticated, DjangoModelPermissionsWithRead]




class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            email = data['email']
            response = super().create(request, *args, **kwargs)
            print(data)
            print(response)
            if response:
                user = User.objects.get(email=email)
                group = Group.objects.get(id=1)
                group.user_set.add(user)
            return response
        except KeyError:
            print("yyy")
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class usernameViewSet(generics.ListAPIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get_queryset(self):
#         username = self.request.GET.get('username')
#         if username:
#             queryset = User.objects.filter(username=username)
#             return queryset

#     def list(self, request):
#         queryset = self.get_queryset()
#         print(queryset)
#         if queryset:
#             return Response(False)
#         return Response(True)


# class loggedInUserUpdate(generics.UpdateAPIView):
    # serializer_class = UserUpdateSerializer
    # permission_classes = [IsAuthenticated]
    # lookup_field = 'id'

    # def get_queryset(self):
    #     queryset = User.objects.filter(id=self.request.user.id)
    #     return queryset

    # def update(self, request, *args, **kwargs):
    #     # partial = kwargs.pop('partial', False)
    #     # print(request.data)
    #     data = request.data
    #     instance = self.get_object()
    #     print(str(instance.id) + "er")
    #     serializer = self.get_serializer(instance, data=data)  # partial=partial)
    #     if serializer.is_valid(raise_exception=True):
    #         self.perform_update(serializer)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # to get token from rest last login
# class CustomLogin(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         result = super().post(request, *args, **kwargs)
#         token = Token.objects.get(key=result.data['token'])
#         update_last_login(None, token.user)
#         return result


# class CustomLogout(APIView):
#     def post(self, request, format=None):
#         header = request.data['headers']
#         tokenn = header['Authorization']
#         actualToken = tokenn[6:]
#         user = Token.objects.get(key=actualToken).user
#         # simply delete the token to force a login
#         user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)
