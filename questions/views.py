from django.shortcuts import render, redirect
from cours.models import Document
from .forms import DocumentSelectionForm
from .utils import generate_questions_from_text
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Question
import json
import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap
from django.contrib.auth.decorators import login_required

@login_required
def generate_questions(request):
    questions = []
    search_term = ''
    question_type_filter = ''

    if request.method == "POST":
        form = DocumentSelectionForm(request.POST)
        if form.is_valid():
            document = form.cleaned_data['document']
            question_type = form.cleaned_data['question_type']
            # Générer les questions
            generated_questions = generate_questions_from_text(document.content, document, question_type)

            if generated_questions:
                questions = generated_questions  # Conservez les questions générées
                # Enregistrer les questions générées dans la session
                request.session['generated_questions'] = [{'content': q.content, 'question_type': q.question_type} for q in questions]
                messages.success(request, f"{len(questions)} questions générées.")
            else:
                messages.warning(request, "Aucune question n'a pu être générée.")
            # Capturez les valeurs de recherche et de filtre
            search_term = request.POST.get('search', '')
            question_type_filter = request.POST.get('question_type_filter', '')

    else:
        form = DocumentSelectionForm()
    
    # Filtrer les questions en fonction des critères de recherche
    if search_term or question_type_filter:
        questions = [
            q for q in questions 
            if (search_term.lower() in q.content.lower() if search_term else True) and
               (q.question_type == question_type_filter if question_type_filter else True)
        ]

    return render(request, 'pages/questions/generate_questions.html', {
        'form': form,
        'questions': questions,
        'search_term': search_term,
        'question_type_filter': question_type_filter,
    })

@csrf_exempt  
@login_required
def save_question(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Charger le corps de la requête en JSON
            content = data.get('content')
            question_type = data.get('question_type')
            document_id = data.get('document_id')

            # Créez une nouvelle question avec le contenu, le type et le document
            question = Question(content=content, question_type=question_type, document_id=document_id)
            question.save()

            return JsonResponse({'status': 'success', 'message': 'Question enregistrée avec succès!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)
@login_required
def export_questions_csv(request):
    # Récupérer les questions générées de la session
    questions = request.session.get('generated_questions', [])

    # Création de la réponse HTTP avec le bon type de contenu
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="questions.csv"'

    # Écriture des questions dans le fichier CSV
    writer = csv.writer(response)
    writer.writerow(['Content', 'Type'])  # Écrire les en-têtes
    for question in questions:
        writer.writerow([question['content'], question['question_type']])  # Écrire chaque question

    return response
@login_required
def export_questions_pdf(request):
    # Récupérer les questions générées de la session
    questions = request.session.get('generated_questions', [])

    # Création d'une réponse HTTP pour le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="questions.pdf"'
    buffer = BytesIO()

    # Création d'un document PDF avec ReportLab
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Écriture du titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Questions Générées")

    # Réinitialisation de la position verticale
    y_position = height - 70
    p.setFont("Helvetica", 10)  # Réduire la taille de la police à 10 points

    # Écriture des questions dans le PDF
    for question in questions:
        content = f"Content: {question['content']}, Type: {question['question_type']}"
        # Gérer les lignes longues
        lines = wrap_text(content, width - 150)  # Ajustez la largeur pour laisser plus d'espace à gauche
        for line in lines:
            p.drawString(50, y_position, line)  # Déplacer les questions à gauche
            y_position -= 12  # Réduire l'espacement entre les lignes
            if y_position < 40:  # Vérifier si on atteint le bas de la page
                p.showPage()  # Commencer une nouvelle page
                p.setFont("Helvetica", 10)
                y_position = height - 50  # Réinitialiser la position

    p.showPage()
    p.save()
    response.write(buffer.getvalue())
    buffer.close()

    return response

def wrap_text(text, max_width):
    """Utilise le module textwrap pour gérer le texte long."""
    # Créer une instance de TextWrapper
    wrapper = textwrap.TextWrapper(width=100)  # Ajustez la largeur pour votre police et votre mise en page
    return wrapper.wrap(text)