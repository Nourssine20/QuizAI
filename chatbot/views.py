import os
import google.generativeai as genai
from django.shortcuts import render
from .forms import MessageForm
from .models import Message

# Configurez l'API avec votre clé
# genai.configure(api_key=os.environ["API_KEY"])
genai.configure(api_key="AIzaSyDdaHPqTF3SaRMV8jSyvP57F79vkm3_cOA")

def chat_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data['user_message']
            bot_response = generate_hint(user_message)  # Utilisation de la nouvelle fonction
            
            Message.objects.create(user_message=user_message, bot_response=bot_response)
    else:
        form = MessageForm()

    messages = Message.objects.all().order_by('-timestamp')
    return render(request, 'pages/chat/chat.html', {'form': form, 'messages': messages})

def generate_hint(question_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Réponds directement à la question suivante : {question_text}"
    response = model.generate_content(prompt)

    if response and hasattr(response, 'text'):
        return response.text
    else:
        return "Aucune réponse générée."

