from django.db import models
import uuid


from cours.models import Document



# Create your models here.
class Question(models.Model):
    QUESTION_TYPES = [
        ('choice', 'Choix Multiple'),
        ('true_false', 'Vrai/Faux'),
        ('open', 'Question Ouverte'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    generated_at = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="questions")
    hint = models.TextField(blank=True) 

    def __str__(self):
        return f"{self.content[:50]}..."