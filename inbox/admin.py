
from django.contrib import admin
from .models import Message, ChatMaster, ChatMessage

# Register your models here.
admin.site.register(Message)
admin.site.register(ChatMaster)
admin.site.register(ChatMessage)