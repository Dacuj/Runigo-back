from django.db import models
from web.models import User
from django.db.models import Max

# Create your models here.
class Message(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
	recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
	body = models.TextField(max_length=1000, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	is_read = models.BooleanField(default=False)

	def send_message(from_user, to_user, body):
		sender_message = Message(
			user=from_user,
			sender=from_user,
			recipient=to_user,
			body=body,
			is_read=True)
		sender_message.save()

		recipient_message = Message(
			user=to_user,
			sender=from_user,
			body=body,
			recipient=from_user,)
		recipient_message.save()
		return sender_message

	def get_messages(user):
		messages = Message.objects.filter(user=user).values('recipient').annotate(last=Max('date')).order_by('-last')
		users = []
		for message in messages:
			users.append({
				'user': User.objects.get(pk=message['recipient']),
				'last': message['last'],
				'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
				})
		return users




class ChatMaster(models.Model):
	participants = models.ManyToManyField(User, related_name='group_member')
    # def __str__(self):
    #     return self.groupName
	# sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
	# recever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')


class ChatMessage(models.Model):
	chat = models.ForeignKey(ChatMaster, related_name="abc", on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_sends")
	content = models.TextField(blank=True)
	timestamp = models.DateTimeField(auto_now=True)