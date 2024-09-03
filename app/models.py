from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    
class GeneratedContent(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class VideoDetail(models.Model):
    generated_content = models.ForeignKey(GeneratedContent, on_delete=models.CASCADE, related_name="video_details",null=False)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=100)
    length = models.IntegerField()
    youtube_link = models.URLField()
    blog = models.TextField(default="null")
    transcript = models.TextField()
    summary = models.TextField()
    publish_date = models.DateField("Published Date")

    def __str__(self):
        return self.title

