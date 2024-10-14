from django.db import models
from django.conf import settings

# Create your models here.

class Course(models.Model):
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    image_url = models.URLField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=80, unique=True)
    link = models.URLField()
    author = models.ForeignKey("authors.Author", related_name="courses", null=True, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    owner = models.ForeignKey('jwt_auth.User', related_name="courses", on_delete=models.CASCADE)


