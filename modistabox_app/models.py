from django.db import models
from authentication_app.models import User


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    created_on = models.DateTimeField(auto_now_add=True)
