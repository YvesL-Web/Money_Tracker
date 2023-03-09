from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user +'s'+'preferences' 
    