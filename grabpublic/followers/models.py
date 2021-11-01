from django.db import models
from profiles.models import UserProfile

# Create your models here.
class Freefollower(models.Model):

    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    free_10_followers = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner)

