from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from rest_framework import viewsets
from .models import ChatMaster, ChatMessage
from .serializers import ChatMasterSErializer, ChatMessageSErializer
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth import get_user_model
User = get_user_model()


class ChatMasterViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMasterSErializer
    queryset = ChatMaster.objects.all()

    def create(self, request, format=None):
        data = request.data
        print('ty')
        print(data)
        textMessage = data['textMessage']
        author = data['author']
        # print(data['participants'])
        # result = []
        # for k in data:
        #     for l in k['participants']:
        #         # print(l)
        #         result.append(l)
        # print(result)
        # pl in  data['participants'])
        serializer = self.get_serializer(data=data)

        # participants = validated_
        if serializer.is_valid():
            gh = serializer.validated_data.get('participants')
            print('gh')
            print(gh)
            print(gh[0].id)
            print(gh[1].id)
            gk = ChatMaster.objects.filter(participants__in = str(gh[0].id))
            dd = ChatMaster.objects.filter(participants__in = str(gh[1].id))

            for k in gk:
                if k in dd:
                    print(k)
                    user = User.objects.get(id=author)
                    ChatMessage.objects.create(content=textMessage, chat = k, author=user)
                    print('done')
                    return Response({"Failure": "dublicate data"}, status=status.HTTP_400_BAD_REQUEST)
            # participants__in = gh[1].id)
            print('gk')
            print(gk)
            # if company_profile.objects.filter(id=request.user.tenant.id):
            #     return Response({"Failure": "Two companies with same tenant not allowed"},
            #                     status=status.HTTP_400_BAD_REQUEST)
            # serializer.save()

            obj = serializer.save()
            objId = obj.id
            self.channel_layer = get_channel_layer()
            content = {
                'command': "new_userChatGroups",
                 'chatGRoup' :  self.ee(ChatMaster.objects.filter(id=objId), objId),
                # "chatGRoup": {
                #     'id': objId,
                #     # 'groupName': objName
                # }
                }


            self.participantsINCHatGroup = ChatMaster.objects.filter(
                id=objId).values_list('participants__id', flat=True)
            # self.room_group_name = 'user_%s' % self.participantsINCHatGroup

            for self.id in self.participantsINCHatGroup:
                self.room_group_name = 'user_%s' % self.id
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'new_chatGroup',
                        'chatGRoup': content
                    }
                )


            user = User.objects.get(id=author)
            ChatMessage.objects.create(content=textMessage, chat = obj, author=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    def ee(self, group, g):
        result = []
        # print(group)
        for d in group:
            r = d.participants.all()
            print('r')
            print(r)

            result.append(self.er(d.participants.all(), g))
            return result

    def er(self, rr, g):
        d = []
        for u in rr:
            d.append(u.username)
        return {
            "username": d,
            "id": g
            # "groupName": group.groupName,
        }






class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSErializer
    queryset = ChatMessage.objects.all()


# class GigViewSet(viewsets.ModelViewSet):
#     serializer_class = GigSErializer
#     queryset = Gig.objects.all()


# class MentorInUniversityViewset(viewsets.ModelViewSet):
#     serializer_class = MentorSErializer
#     queryset = Mentors.objects.all()


#     def list(self, request):
#         universityId = request.GET.get('uniId')
#         if universityId is not None:
#             # print(universityId)
#             # print('universityId')
#             # print(self.request.user)
#             # queryset = Mentors.objects.filter(mentor=self.request.user, universities = universityId)
#             queryset = Mentors.objects.filter(universities = universityId)
#             # print(queryset)
#         else:
#             # print('ggggggggggggggggggg')
#             queryset = Mentors.objects.all()
#         serializer = MentorSErializer(queryset, many=True)
#         return Response(serializer.data)


