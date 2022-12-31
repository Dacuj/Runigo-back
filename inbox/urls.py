from django.urls import path
from inbox.views import Inbox, UserSearch, Directs, NewConversation, SendDirect, IndividualChat
from rest_framework.routers import DefaultRouter
from .apiVIews import ChatMasterViewSet, ChatMessageViewSet

router=DefaultRouter()
router.register('chatMaster', ChatMasterViewSet, basename='Chat Master')
router.register('chatMessage', ChatMessageViewSet, basename='Chat Message')


urlpatterns = [
   	path('', Inbox, name='inbox'),
   	path('inbox/<username>', Directs, name='directs'),
   	path('new/', UserSearch, name='usersearch'),
   	path('new/<username>', NewConversation, name='newconversation'),
   	path('send/', SendDirect, name='send_direct'),

	path('individualChat/<username>', IndividualChat, name="individualChat")

]



urlpatterns += router.urls
