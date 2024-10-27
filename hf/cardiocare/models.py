from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # Add name field
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Add profile picture field

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class HealthData(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s Health Data"