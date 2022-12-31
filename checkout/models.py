from django.db import models
from django.core import validators
import uuid
from django.db.models.signals import pre_save
from web.models import Mentors



class OrderDetail(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )
    
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)

    # You can change as a Foreign Key to the user model
    customer_email = models.EmailField(
        verbose_name='Customer Email'
    )

    gig = models.ForeignKey(
        to=Mentors,
        verbose_name='Product',
        on_delete=models.PROTECT
    )

    amount = models.IntegerField(
        verbose_name='Amount'
    )

    # This field can be changed as status
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.uuid}"
