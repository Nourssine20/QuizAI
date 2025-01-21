# forms.py
from django import forms
from cours.models import Document

class DocumentSelectionForm(forms.Form):
    document = forms.ModelChoiceField(queryset=Document.objects.all(), label="Sélectionnez un Document")
    question_type = forms.ChoiceField(
        choices=[
            ('choice', 'Choix Multiple'),
            ('true_false', 'Vrai/Faux'),
            ('open', 'Question Ouverte'),
        ],
        label="Type de Question"
    )
