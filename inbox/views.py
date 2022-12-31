from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

from django.contrib.auth.decorators import login_required

from web.models import User
from inbox.models import Message


from .models import ChatMaster, ChatMessage




from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

@login_required
def Inbox(request):
	messages = Message.get_messages(user=request.user)
	active_direct = None
	directs = None

	if messages:
		message = messages[0]
		active_direct = message['user'].username
		directs = Message.objects.filter(user=request.user, recipient=message['user'])
		directs.update(is_read=True)
		for message in messages:
			if message['user'].username == active_direct:
				message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct': active_direct,
		}

	template = loader.get_template('inbox/directs.html')

	return HttpResponse(template.render(context, request))

@login_required
def UserSearch(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query))

		#Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users': users_paginator,
			}
	
	template = loader.get_template('inbox/search_user.html')
	
	return HttpResponse(template.render(context, request))

@login_required
def Directs(request, username):
	user = request.user
	messages = Message.get_messages(user=user)
	active_direct = username
	directs = Message.objects.filter(user=user, recipient__username=username)
	directs.update(is_read=True)
	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct':active_direct,
	}

	# return render(request, "inbox/individualChat.html", context)
	template = loader.get_template('inbox/directs.html')

	return HttpResponse(template.render(context, request))


@login_required
def NewConversation(request, username):
	print(request)
	print(username)
	if request.method == "POST":
		print("asd")
		from_user = request.user
		body = request.POST["body"]
		try:
			to_user = User.objects.get(username=username)
			print("aaaaaaaaasd")
		except Exception as e:
			print("asdeeeeeeeee")
			return redirect('usersearch')
		if from_user != to_user:
			print("asdddddddd")
			Message.send_message(from_user, to_user, body)
		return redirect('inbox')

@login_required
def SendDirect(request):
	print(request)
	from_user = request.user
	to_user_username = request.POST.get('to_user')
	body = request.POST.get('body')
	
	if request.method == 'POST':
		to_user = User.objects.get(username=to_user_username)
		Message.send_message(from_user, to_user, body)
		return redirect('inbox')
	else:
		HttpResponseBadRequest()

def checkDirects(request):
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()

	return {'directs_count':directs_count}




@login_required
def IndividualChat(request, username):
	user = request.user
	# print("helllllll")
	# print(username)
	# print(user)
	# print("tttttttt")

	reciever = User.objects.get(username = username)

	# print(reciever)

	try:
		chatMasterId =  ChatMaster.objects.get(sender = user, recever=reciever)
		print(chatMasterId)
	except ChatMaster.DoesNotExist:
		chatMasterId = None

	print(chatMasterId.id)


	# print(ChatMaster.objects.all())


	messages = Message.get_messages(user=user)
	active_direct = username
	directs = Message.objects.filter(user=user, recipient__username=username)
	directs.update(is_read=True)
	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct':active_direct,
	}

	return render(request, "inbox/individualChat.html", context)