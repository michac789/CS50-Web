from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class FollowPair(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    
    def __str__(self):
        return f"{self.follower} follows {self.following}"

class Post(models.Model):
    title = models.CharField(max_length = 64)
    content = models.CharField(max_length = 1024)
    likes = models.IntegerField(max_length = 16)
    time = models.DateTimeField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id}: {self.title}, posted by: {self.poster}, {self.likes} likes."

class Comment(models.Model):
    comment = models.CharField(max_length = 256)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id}: {self.comment}"
