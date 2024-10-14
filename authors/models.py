from django.db import models

# Create your models here.

class Author(models.Model):
    def __str__(self):
        return f"{self.name}-{self.email}"
    
    name = models.CharField(max_length=80, unique=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=50, unique=True, default='cheahhonyuen@gmail.com')
    
