from django.db import models

class Paste(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=True)

