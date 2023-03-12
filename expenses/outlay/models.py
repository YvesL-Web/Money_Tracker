from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Outlay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    category = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    date = models.DateTimeField(default= datetime.now,)

    def __str__(self):
        return self.category
    
    class Meta:
        ordering = ['-date']

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'