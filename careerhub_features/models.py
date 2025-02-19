from django.db import models
from userauthapp.models import User

# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=100)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class UserQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'question']

    def __str__(self):
        return f"{self.user.username} - {self.question.title}"

class Resume(models.Model):
    imglink = models.URLField(max_length=200)
    title = models.CharField(max_length=100)
    description = models.TextField()
    hreflink = models.URLField(max_length=200)
    pick = models.CharField(max_length=50)
    authorname = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Roadmap(models.Model):
    fieldname = models.CharField(max_length=100)
    roadmaplink = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fieldname
