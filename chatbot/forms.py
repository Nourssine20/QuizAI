from django import forms

class MessageForm(forms.Form):
    user_message = forms.CharField(label='Votre message', max_length=500)