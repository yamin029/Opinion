from django.db import models
# importing USER as the django has build in to it
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(max_length=200, null=True)
    
    avatar = models.ImageField(null=True, default='avatar.svg')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    

# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null=True)# we want to keep the room even after deleting the topic
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True) #letting django know that this field can be blank and can be saved blank as well
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)# while we quarrying data for participants this related_name wold help us to quarry from the DB.
    
    class Meta:
        # we are setting the order of the rooms. "-" means the last item puts in the first
        ordering = ['-updated','-created']
    
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.CASCADE) # cascade means we want to delete the message as well after deleting the room
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.body[0:50]
    
    