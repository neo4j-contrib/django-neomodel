from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class SNCUser(models.Model):
    snc_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    user_name = models.CharField(max_length=100, default="randomSNCuser")
    user_password = models.CharField(max_length=100, default="password")
    user_id = models.IntegerField(default=-1)
    access_level = models.TextField(default="user")
    date_added = models.DateTimeField(default=timezone.now)
    last_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user_name
