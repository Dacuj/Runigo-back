from rest_framework import viewsets
from .models import University, Mentors, FavMentor
from users.models import User
from .models import Comments as CommentsModel
from .serializers import UniversitySErializer, MentorSErializer, CommentsSerializer, FavMentorSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser
from chatapp.permission import DjangoModelPermissionsWithRead
from rest_framework import status
from django.contrib.auth.models import Group
from rest_framework.parsers import MultiPartParser, FormParser

class UniversityViewSet(viewsets.ModelViewSet):
    serializer_class = UniversitySErializer
    queryset = University.objects.all()
    # permission_classes = [IsAuthenticated]#, IsAdminUser]
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        # elif self.action == "create":
        #     permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class FavMentorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithRead]
    serializer_class = FavMentorSerializer
    queryset = FavMentor.objects.all()




# class GigViewSet(viewsets.ModelViewSet):
#     serializer_class = GigSErializer
#     queryset = Gig.objects.all()

# class GigInMentor(viewsets.ModelViewSet):
#     serializer_class = GigSErializer
#     queryset = Gig.objects.all()

#     def list(self, request):
#         mentorId = request.GET.get("mentorId")

#         if mentorId is not None:
#             queryset = Gig.objects.filter(gigger = mentorId)

#         else:
#             queryset = Gig.objects.all()
#         serializer = GigSErializer(queryset, many=True)
#         return Response(serializer.data)


class MentorViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = MentorSErializer
    queryset = Mentors.objects.all()
    # permission_classes = [IsAuthenticated, DjangoModelPermissionsWithRead]

    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = request.data
            userId = data['mentor']
            user = User.objects.get(id=userId)
            groupToRemove = Group.objects.get(id=1)
            groupToAdd = Group.objects.get(id=2)
            print(groupToRemove)
            print(user)
            try:
                user.groups.remove(groupToRemove)
                user.groups.add(groupToAdd)
            except:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        user = request.GET.get("user")
        print(user)
        if user is not None:
            print(user)
            queryset = Mentors.objects.filter(mentor__username=user)
        else:
            queryset = Mentors.objects.all()
            
                    # serializer = (data=request.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     try:
    #         data = request.data
    #         tenant = data['user']
    #         response = super().create(request, *args, **kwargs)
    #         if response:
    #             user = User.objects.filter(email=email)
    #             # userId = User.objects.get(email=email).id
    #             userId = response.id
    #             if tenant:
    #                 user.update(userfrom="1")
    #             else:
    #                 user.update(userfrom="2")
    #                 # user.update(branch=branchId, , tenant=tenant)
    #             empMasterr.objects.create(user=response, branch=branchId, user_group=userGroup, tenant=tenant)
    #             groupIdFromUserGroup = user_group.objects.get(id=userGroup).group.id
    #             group = Group.objects.get(id=groupIdFromUserGroup)
    #             group.user_set.add(userId)
    #         return response
    #     except KeyError:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)





class MentorInUniversityViewset(viewsets.ModelViewSet):
    serializer_class = MentorSErializer
    queryset = Mentors.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithRead]


    def list(self, request):
        universityName = request.GET.get('uniName')
        if universityName is not None:
            # print(universityId)
            # print('universityId')
            # print(self.request.user)
            # queryset = Mentors.objects.filter(mentor=self.request.user, universities = universityId)
            queryset = Mentors.objects.filter(universities__name = universityName)
            # print(queryset)
        else:
            # print('ggggggggggggggggggg')
            queryset = Mentors.objects.all()
        serializer = MentorSErializer(queryset, many=True)
        return Response(serializer.data)

class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    queryset = CommentsModel.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithRead]


class CommentsInMentorsViewset(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    queryset = CommentsModel.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissionsWithRead]

    def list(self, request):
        mentorId = request.GET.get("mentorId")
        user = request.GET.get("user")
        if mentorId is not None:
            queryset = CommentsModel.objects.filter(mentor = mentorId)
        elif user is not None:
            print(user)
            mentor = Mentors.objects.get(mentor__username=user)
            print(mentor)
            queryset = CommentsModel.objects.filter(mentor = mentor)
        else:
            queryset = CommentsModel.objects.all()
        serializer = CommentsSerializer(queryset, many=True)
        return Response(serializer.data)

