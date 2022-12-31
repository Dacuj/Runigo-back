import json
# import json5
# from unittest import result
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import ChatMaster, ChatMessage


User = get_user_model()


class ChatConsumer(WebsocketConsumer):
# class ChatConsumer(AsyncWebsocketConsumer):

    print("rrrrrrrrrrrrrrr")

    def connect(self):

        print("aaaaaaaa")

        self.room_name = self.scope['url_route']['kwargs']['room_name']

        self.room_group_name = 'user_%s' % self.room_name
        print(self.room_group_name)
        # userIdFromUrl = self.room_name
        # print(self.room_group_name)




        # print('session')
        # print(self.scope["session"])

        # print(self.room_name)
        # print('user')
        # print(self.scope["user"])



        # GroupUserIsPartticiantIn = ChatGroup.objects.filter(
        #     participants__id=userIdFromUrl).values_list("id", flat=True)
        # print(GroupUserIsPartticiantIn)
        # dataaas={"groupId": [id for id in GroupUserIsPartticiantIn]}
        # print(dataaas)
        # print(self.user)
        # print(self.room_group_name)

                    # group = {"name" : self.room_name, 'participants': self.room_name}

                    # print(group)

        # Join room group
        # user is joined to all the chatgroup he is present in
        # for group in GroupUserIsPartticiantIn:
        # print("chatGroup"+str(group))


        # print(self.room_group_name)
        # print(self.channel_name)


        async_to_sync(self.channel_layer.group_add)(
            # "chatGroup"+str(group),
            self.room_group_name,
            self.channel_name
        )

        # self.user = self.scope["user"]
        
        # if self.user.is_authenticated:
        #     self.accept()
        # else:
        #     self.close()

        self.accept()



    # def activeChats(self, data):
    #     self.userId = data['userId']
    #     self.activeChatss = ChatSession.objects.all()

    #     content = {
    #         'command': "activeSessions",
    #         'actveSession': self.Sessions(self.activeChatss)
    #     }
    #     self.send_message(content)

    # def Sessions(self, sessions):
    #     result = []
    #     for session in sessions:
    #         result.append(self.eachSession(session))
    #     return result

    # def eachSession(self, session):
    #     # print(message.chatGroup.id)
    #     return {
    #         "id": session.id,
    #         "sessionName": session.name,
    #     }


    def userChatGroups(self, data):
        self.userId = data['userId']
        self.userChats = ChatMaster.objects.filter(participants__id=self.userId)
        for k in self.userChats:
            df = ChatMaster.objects.filter(id=k.id)
            for d in df:
                r = d.participants.all()
                for l in r:
                    print(l)
                # print(l.username for l in r)

        # self.par =       ChatMaster.objects.filter(id=self.userId).values_list('participants__id', flat=True)

        print("fgfgfg")
        print(self.userChats)
        # print(self.userChats)
        content = {
            'command': "userChatGroups",
            # 'chatGRoups': self.chatGroups(self.userChats),
            'chatInfo' : self.users(self.userChats),
            # 'user' : l.username for l in d.participants.all()  
        }
        self.send_message(content)

    def users(self, groups):
        result = []
        for g in groups:
            result.append(self.ee(ChatMaster.objects.filter(id=g.id), g))
            # print(result)
        return result


    def ee(self, group, g):
        result = []
        # print(group)
        for d in group:
            # print(d)
            r = d.participants.all()
            result.append(self.er(d.participants.all(), g))
            print('r')
            print(result)
            print(r)
            print('uuii')
            return result
            # for l in r:
            #     print(l)
        # print(message.chatGroup.id)
            # return {
            #     "id": l.username for l in r
            #         # "groupName": group.groupName,
            # }

    def er(self, rr, g):
        print('rr')
        print(rr)
        d = []
        for u in rr:
            d.append(u.username)
            print('u')
            print(d)
            print("op")
            print(u)
        return {
            "username": d,
            "id": g.id
            # "groupName": group.groupName,
        }


    def chatGroups(self, groups):
        result = []
        for group in groups:
            result.append(self.eachGroup(group))
            print(result)
        return result

    def eachGroup(self, group):
        # print(message.chatGroup.id)
        return {
            "id": group.id,
            # "groupName": group.groupName,
        }

    def fetch_messages(self, data):
        print('data')
        print(data)
        # messages = Message.last_30_message()
        messages = ChatMessage.objects.filter(
            chat=data['chatGroup']).all()[:30]
            # order_by("-timestamp")
        content = {
            "command": 'messages',
            "messages": self.messages_to_json(messages)
        }
        self.send_message(content)
        # pass

    def new_message(self, data):
        # print(data)
        # print("rv")
        # print(data['message'])
        # print(data)
         # print(self)
        message = data['message']
        author = data['from']
        # chatGroup=data['chatGroup']

        # print(author)
        # print(chatGroup)
        chatGroup = ChatMaster.objects.filter(id=data['chatGroup'])[0]
        author_user = User.objects.filter(id=author)[0]
        message = ChatMessage.objects.create(
            author=author_user,
            # author=author,
            # content=data['message'],
            content=message,
            chat=chatGroup
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)
        # print("new message")
        # pass


    #     # for websockewt
    #     content = {
    #         'command': 'new_message',
    #         'message': data
    #     }
    #     return self.send_chat_message(content)


    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        # print(message.chatGroup.id)
        return {
            "id": message.id,
            "author": message.author.username,
            "content": message.content,
            "timestamp": str(message.timestamp),
            "chatGroup": str(message.chat.id)
        }


    # def currentGroup(self, data):
    #     print(data)
    #     print("self")
    #     print(self)



    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message,
        "userChatGroups": userChatGroups,
        # "activeChats": activeChats,
        # "currentGroup" : currentGroup
    }

    

    def disconnect(self, close_code):
        print('rrrvvv')
        print(close_code)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("ranuVIjay")
        # text_data=None,
        # print(text_data['command'])

        # my_json = json.dumps(text_data)

        # py_obj = json.loads(text_data)
        # print(my_json)
        # print(my_json["command"])
        # d= json.dumps(text_data)
        # print('d')
        data = json.loads(text_data)
        # print(self.commands[data["command"]])

        print(data)

        # print('drt')
        # print(data['command'])
        # if data['command'] == "new_message":
        #     data1 = json.loads(bytes_data)
        #     print(data1)

        # print(data["message"])
        # async_to_sync
        self.commands[data["command"]](self, data)
                # message = data['message']

        # Send message to room group

    def send_chat_message(self, message):
        # print("Ranu")
        # print(message)
        # print((message['message'])['chatGroup'])

        self.chatGroupId = (message['message'])['chatGroup']

        self.participantsINCHatGroup = ChatMaster.objects.filter(
            id=self.chatGroupId).values_list('participants__id', flat=True)
        # self.room_group_name = 'user_%s' % self.participantsINCHatGroup

        # print(participantsINCHatGroup)
        # print((message['message'])['chatGroup'])
        # print(self.channel_name)

        # user is joined to all the groups he is participants in
        # find the current group from the chat itself and send to all the users of that group
        # groupToSend = "chatGroup"+str((message['message'])['chatGroup'])

        for self.id in self.participantsINCHatGroup:
            self.room_group_name = 'user_%s' % self.id
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

        # for self.id in self.participantsINCHatGroup:
            # self.room_group_name = 'user_%s' % self.id

        # self.room_group_name = 'user_%s' % self.room_name

        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )

    def send_message(self, message):
        print("a")
        self.send(text_data=json.dumps(message))

    # # Receive message from room group

    def new_chatGroup(self, event):
        # //this comes from creating the chat group
        # this comes from chatgroup create
        chatGRoup = event['chatGRoup']
        self.send(text_data=json.dumps(chatGRoup))


    # def new_chatSession(self, event):
    #     # //this comes from creating the chat group
    #     # this comes from chatgroup create
    #     chatSession = event['chatSession']
    #     self.send(text_data=json.dumps(chatSession))



    def chat_message(self, event):
        message = event['message']
        print("c")
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
