from django.db import models
import uuid
from django.contrib.auth.models import User
from quiz.models import Test

# Create your models here.
class Performance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    average_score = models.FloatField(default=0.0)
    tests_taken = models.IntegerField(default=0)
    last_test_score = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="performances")
    test = models.ForeignKey(Test, on_delete=models.CASCADE,null=True, related_name="performances")
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Performance of {self.user}"

class Recommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name="recommendations")

    def __str__(self):
        return f"Recommendation for {self.performance.user}"