from django.db import models
from django.contrib.auth.models import User
# from django.utils.timezone import now
from datetime import datetime

# Create your models here.
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    source = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    date = models.DateTimeField(default= datetime.now)

    def __str__(self):
        return self.source
    
    class Meta:
        ordering = ['-date']

class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    