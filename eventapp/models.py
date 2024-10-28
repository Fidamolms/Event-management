# eventapp/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # Add any other fields you need for your custom user model

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    # Add any other profile-specific fields you need

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/')  # Ensure you have a media folder set up

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"{self.event_name} booked by {self.user.username}"

def get_default_image():
    # Ensure you have an image in your media folder named 'default_event_image.jpg'
    return os.path.join(settings.MEDIA_URL, 'default_images/default_event_image.jpg')
