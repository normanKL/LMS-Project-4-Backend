from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    email = models.CharField(max_length=50, unique=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    quote = models.TextField(null=True, blank=True)
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True) 
    country = models.CharField(max_length=100, default='Unknown')
    quote = models.TextField(default='Quote')
    courses = models.ManyToManyField('courses.Course')
    

    def __str__(self):
        return self.user.username