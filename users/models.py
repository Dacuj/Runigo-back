
from django.db import models
from django.contrib.auth.models import AbstractUser

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class User(AbstractUser):
    is_mentor = models.BooleanField(default=False)
    # balance = models.DecimalField(verbose_name='balance', decimal_places=2, max_digits=10)
    profile_pic = models.ImageField(upload_to=upload_to, default='images/default.webp')
    # models.ImageField(upload_to='pics', default=, width_field=150px)



