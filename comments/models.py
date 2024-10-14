from django.db import models

# Create your models here.

class Comment(models.Model):
    def __str__(self):
        return f"{self.course} - {self.created_at}"
    
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey("courses.course", related_name="comments", on_delete=models.CASCADE)
    owner = models.ForeignKey('jwt_auth.User', related_name="comments", on_delete=models.CASCADE)
    