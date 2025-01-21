# utils.py
import google.generativeai as genai
from .models import Question
import os

# Configurez l'API avec votre clé
genai.configure(api_key="AIzaSyDdaHPqTF3SaRMV8jSyvP57F79vkm3_cOA")

def generate_questions_from_text(content, document, question_type):
    """
    Utilise Gemini Flash 1.5 pour générer des questions à partir du texte du document
    en fonction du type de question sélectionné et les enregistre dans la base de données.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Préparer la requête pour l'IA en fonction du type de question
    if question_type == 'open':
        prompt = (
            f"Generate 10 one-line open questions from this content: {content}\n"
            "Only return questions in the format: {Generated Question}.\n"
            "Do not include any other text."
        )
    elif question_type == 'true_false':
        prompt = (
            f"Generate 10 true/false questions from this content. Each question must be formatted as:\n"
            "{Generated Question? True or False}\n"
            "Only return questions in this format. Do not include any other text.\n"
            f"{content}\n"
        )
    elif question_type == 'choice':
        prompt = (
            f"Generate 10 multiple-choice questions with one question and four answer options from this content:\n"
            "Format the output as follows:\n"
            "{Generated Question} a) {1st Option} b) {2nd Option} c) {3rd Option} d) {4th Option}\n"
            "Only return questions in this format. Do not include any other text.\n"
            f"{content}\n"
        )

    # Générer le contenu
    response = model.generate_content(prompt)
    
    questions = []
    
    if response and hasattr(response, 'text'):
        questions_text = response.text.strip().splitlines()
        for question_text in questions_text:
            question_text = question_text.strip()
            if question_text:
                # Remove curly braces from the question text
                question_text = question_text.replace("{", "").replace("}", "").strip()

                # Create an instance of Question without saving
                questions.append(Question(content=question_text, question_type=question_type, document=document))

    return questions
