from django.db import models

# Create your models here.

    
class GeneratedContent(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class VideoDetail(models.Model):
    generated_content = models.ForeignKey(GeneratedContent, on_delete=models.CASCADE, related_name="video_details",null=False)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=100)
    length = models.IntegerField()
    description = models.TextField(null=True)
    publish_date = models.DateField("Published Date")

    def __str__(self):
        return self.title

