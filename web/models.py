# from email.policy import default
# from queue import Empty
# from tkinter import CASCADE
# from tokenize import blank_re
from unicodedata import name
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date


from django.contrib.auth import get_user_model
User = get_user_model()



class University(models.Model):
    name = models.CharField(max_length=64)
    coverimage = models.CharField(max_length=192, blank=True)
    
    def __str__(self):
        return f"{self.name}"


class Mentors(models.Model):
    mentor = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mentor")
    universities = models.ManyToManyField(University, blank=True, related_name="universities")
    school_email = models.EmailField(null=True)
    nationality = models.CharField(max_length=64, null=True)
    bio = models.TextField(blank=True)
    price = models.DecimalField(verbose_name='Price', decimal_places=2, max_digits=6)
    

    def __str__(self):
        return f"{self.mentor}, id:{self.id}"


# class Gig(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     gigger = models.ForeignKey(Mentors, on_delete=models.CASCADE, related_name="gigger")    
#     description = models.TextField(blank=True, max_length=800, verbose_name='Description')
   

#     def __str__(self):
#        return f"{self.gigger}, ${self.price}, id:{self.id}"


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    mentor = models.ForeignKey(Mentors, on_delete=models.CASCADE, related_name="comment_mentor")
    comment = models.TextField(blank=True)
    stars = models.PositiveSmallIntegerField()
    time = models.DateTimeField(auto_now=True)


class FavMentor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    FavouriteMentors = models.ManyToManyField(Mentors)