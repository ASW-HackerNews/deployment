from email.policy import default
from enum import Flag
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#TODO: podriamos poner validators

class Post(models.Model):

   content = models.TextField(null=True, blank=True)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   likes = models.IntegerField(default=0)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return str(self.id)

class Ask(Post):
   title = models.CharField(max_length=200, null=False, blank=False)

   def __str__(self):
      return self.title

class Link(Post):
   url = models.URLField(max_length=200)
   title = models.CharField(max_length=200, null=False, blank=False)

   def __str__(self):
      return self.title

class Like(models.Model):
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   liked_by = models.ForeignKey(User, on_delete=models.CASCADE)


   def __str__(self):
      return f'{self.post} , {self.liked_by}' 

class Comment(Post):
   commented = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commented_post")

   def __str__(self):
        return self.content