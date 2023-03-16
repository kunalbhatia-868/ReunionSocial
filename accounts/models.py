import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from accounts.utils import LowercaseEmailField
from accounts.managers import UserProfileManager
# Create your models here.

class UserProfile(AbstractUser):
    user_id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    username=models.CharField(_('username'),max_length=200)
    email=LowercaseEmailField(_('email address'),unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last_name"), max_length=150)
    bio=models.TextField(blank=True)
    follower_count=models.PositiveBigIntegerField(default=0)
    following_count=models.PositiveBigIntegerField(default=0)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects=UserProfileManager()

    def __str__(self):
        return self.email
    
class Following(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    sender=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="sender")
    reciever=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="reciever")
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.reciever.username}"