from django.db import models
from django.contrib.auth.models import User

class FavoriteTeam(models.Model):
    TeamID = models.IntegerField(null=True)
    user = models.OneToOneField(User,related_name="TeamID", on_delete=models.CASCADE, null=True)

