from django import forms
from .models import Document

class CoursForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'content', 'fichier']  # Enlève type_ajout et lien

    def clean(self):
        cleaned_data = super().clean()
        fichier = cleaned_data.get("fichier")

        if not fichier:
            raise forms.ValidationError("Vous devez téléverser un fichier.")
        return cleaned_data