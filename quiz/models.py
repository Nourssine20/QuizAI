from django.db import models
import uuid
from django.contrib.auth.models import User

from questions.models import Question

# Create your models here.
class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()  # en minutes
    questions = models.ManyToManyField(Question, related_name="tests")
    taken_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tests")

    def __str__(self):
        return self.title
class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    response_content = models.TextField()
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")

    def __str__(self):
        return f"Response by {self.user} on {self.submitted_at}"
class UserFeedback(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='feedbacks')
    user_comment = models.TextField(blank=True)
    helpful = models.BooleanField(default=False)

