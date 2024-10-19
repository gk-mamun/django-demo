from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Run(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=255)
    json_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
