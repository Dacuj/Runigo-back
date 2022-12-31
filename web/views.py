from django.shortcuts import render
from django.core.mail import send_mail
# from curses.ascii import HT
import time
from cgitb import text
import json
from telnetlib import STATUS
from urllib.request import HTTPErrorProcessor
from django import http
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import University, User, Mentors

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'web/index.html')
    else:
        return render(request, 'web/index.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "web/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "web/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "web/register.html", {
                "message": "Passwords must match."
            })

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        # Attempt to create new user
        #check if user email exists
        try:
            email_exists = User.objects.get(email= email)
            return render(request, "web/register.html", {
                "message": "This email is already associated to an account"
            })
        except ObjectDoesNotExist:
            pass
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "web/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        #sending registration successful email
        # send_mail(
        #     'Registration Successful',
        #     f'Good job {username}',
        #     settings.EMAIL_HOST_USER,
        #     [email],
        #     fail_silently=False,
        # )


        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "web/register.html")

def supportedunis(request):
    universities = University.objects.all()
    return render(request, "web/supportedunis.html", {"universities": universities})

def universities(request, university):
    #check if the university exists
    try:
        print(university)
        uni = University.objects.get(name = university)

        #check if the user is a mentor and excluding it later on
        if request.user.is_authenticated:
            try:
                print(request.user)
                print(uni)
                mentor = Mentors.objects.get(mentor=request.user, universities = uni)
                print(mentor)
            except ObjectDoesNotExist:
                mentor = False
        else:
            print('request.user')
            mentor = ""

        #get all the mentors
        mentors = Mentors.objects.filter(universities = uni)

        print(mentors)


        #rendering the template 
        return render(request,"web/university.html", {"uni": uni, "mentor": mentor, "mentors": mentors})

    except ObjectDoesNotExist:
        return HttpResponse("Your university is not supported yet :|")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def becomeamentor(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "web/becomeamentor.html")

def mentorprofile(request, mentorname):
    #checking if the user is a mentor
    print('requesttttttttttttttttttttttttt')
    print(request)
    print(mentorname)
    try:
        user = User.objects.get(username = mentorname)
        mentor = Mentors.objects.get(mentor = user)

        print(user)
        print(mentor)
        #checking if the user has any active gig
        try:
            # gig = Gig.objects.get(gigger = mentor)
            gig =""
            print("gig")
            return render(request, "web/mentorprofile.html", {"mentor": mentor, "userz": user, "gig":gig})
        except ObjectDoesNotExist:
            print("gigi")
            return render(request, "web/mentorprofile.html", {"mentor": mentor, "userz": user})

    except ObjectDoesNotExist:
        return HttpResponse("Ciaone")

@login_required
def accountedit(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "web/editaccount.html", {"user": request.user})

@login_required
def checkout(request):
    return HttpResponse("Stripe implementation")