from django.db import models
import uuid 
from accounts.models import UserProfile
# Create your models here.


class Post(models.Model):
    post_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='posts')
    title=models.TextField(blank=True)
    description=models.TextField(blank=True)
    like_count=models.PositiveBigIntegerField(default=0)
    comment_count=models.PositiveBigIntegerField(default=0)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return  f"{self.user.username}"  

class Comment(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    text=models.TextField(blank=True)
    created_on=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return  f"{self.user.username} - {self.text[:10]}"   



class Like(models.Model):           
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return  f"{self.user.username}-{self.post}"


