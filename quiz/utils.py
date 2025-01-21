import google.generativeai as genai
import os

# Configurez l'API avec votre clé
# genai.configure(api_key=os.environ["API_KEY"])
genai.configure(api_key="AIzaSyDdaHPqTF3SaRMV8jSyvP57F79vkm3_cOA")

def generate_hint(question_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Generate a hint for the question: {question_text}")
    
    if response and hasattr(response, 'text'):
        return response.text
    else:
        return "Aucun indice généré."