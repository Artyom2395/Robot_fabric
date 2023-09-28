from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    email = models.CharField(max_length=255,blank=False, null=False)

class Director(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_director = models.BooleanField(default=False)
   
    def __str__(self):
        return self.user.username