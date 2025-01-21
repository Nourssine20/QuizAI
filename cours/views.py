from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Document
from .forms import CoursForm
import google.generativeai as genai
from django.core.paginator import Paginator
from django.http import JsonResponse
import markdown2
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def indexCours(request):
    
    return render(request, 'pages/cours/index.html')
genai.configure(api_key="AIzaSyDdaHPqTF3SaRMV8jSyvP57F79vkm3_cOA")


# def generate_course(request):
#     if request.method == "POST":
#         title = request.POST.get("titre")  # Récupérer le titre du formulaire

#         model = genai.GenerativeModel("gemini-1.5-flash")

#         # Créer le prompt en utilisant le titre
#         prompt = (
#             f"Générer un cours détaillé sur le sujet : '{title}'. Structure le cours avec des titres clairs, des sous-titres, et des listes à puces. Utilise des analogies simples pour expliquer des concepts complexes.\n\n"
#             "Présente le contenu de manière visuelle et attrayante en intégrant des *tableaux comparatifs*, *schémas de structure*, et *diagrammes de flux* pour illustrer chaque concept clé, sans utiliser de photos. Inclure notamment :\n\n"
#             "1. *Tableaux Comparatifs* : Pour des sections comme Avantages et Inconvénients et Types, ajoute des tableaux qui comparent les concepts ou lister leurs caractéristiques et utilisations.\n\n"
#             "2. *Schémas et Diagrammes* : Pour des sujets comme le schéma de {title}, les requêtes et mutations, et les cas d’usage, intègre des diagrammes ou schémas pour faciliter la compréhension.\n\n"
#             "Je veux une présentation belle, professionnelle et structurée. Cela signifie que le contenu doit être affiché de manière claire et attrayante, avec un agencement soigné, des graphiques pertinents, des couleurs adaptées, et une organisation logique pour faciliter la compréhension.\n\n"
#             "Affiche des éléments visuels comme des tableaux, des schémas, et des graphes pour illustrer les concepts, mais sans utiliser de photos.\n\n"
#             "1. *Introduction :* Présenter le sujet et les objectifs du cours.\n"
#             "2. *Chapitres clés ou sujets (au moins 3 sections) :* Détails de chaque sujet avec des sous-sections si nécessaire, incluant des exemples concrets.\n"
#             "3. *Exemples pratiques ou études de cas :* Illustrer les concepts abordés par des cas d'utilisation réels.\n"
#             "4. *Conclusion :* Récapituler les points principaux et fournir des conseils pour aller plus loin.\n\n"
#             "Veuillez également inclure des suggestions de références pertinentes avec des liens dynamiques et à jour, tels que des livres, des sites web, et d'autres ressources supplémentaires pour l'apprentissage continu.\n\n"
#             "Le cours doit être informatif, bien structuré, et adapté à un public débutant à intermédiaire. Veuillez rendre le texte visuellement attractif en utilisant des éléments de mise en forme appropriés, comme des listes, des titres, des paragraphes clairs, et des couleurs pour différencier les sections."
#         )

#         # Générer le contenu du cours
#         response = model.generate_content(prompt)
#         generated_course = response.text
#         html = markdown.markdown(generated_course)
#         print(html)
#         # Enregistrer le cours dans la base de données
#         new_cours = Document(title=title, content=generated_course)
#         new_cours.save()

#         return render(
#             request,
#             "pages/cours/generate_cours.html",
#             {"title": title, "generated_course": generated_course},
#         )

#     # Afficher le formulaire si la méthode n'est pas POST
#     return render(request, "pages/cours/generate_form.html")
    # return HttpResponse(f"<h1>Course: {title}</h1><pre>{generated_course}</pre>")
def generate_course(request):
    if request.method == "POST":
        title = request.POST.get("title")  # Récupérer le titre du formulaire

        model = genai.GenerativeModel("gemini-1.5-flash")

        # Créer le prompt en utilisant le titre
        prompt = (
            f"Générer un cours détaillé sur le sujet : '{title}'. Structure le cours avec des titres clairs, des sous-titres, et des listes à puces."
            " Utilisez des analogies simples pour expliquer des concepts complexes.\n\n"
            "Inclure des graphiques, des schémas, et des liens dynamiques vers des ressources supplémentaires pour enrichir le contenu.\n\n"
            "Le contenu doit être structuré de manière visuelle avec un agencement soigné :\n"
            "1. Introduction : Présenter le sujet et les objectifs du cours.\n"
            "2. Chapitres clés ou sujets (au moins 3 sections) : Détails de chaque sujet avec des sous-sections si nécessaire, incluant des exemples concrets.\n"
            "3. Exemples pratiques ou études de cas : Illustrer les concepts abordés par des cas d'utilisation réels.\n"
            "4. Conclusion : Récapituler les points principaux et fournir des conseils pour aller plus loin.\n"
            "Pour chaque section :\n"
            "- Inclure des suggestions de références pertinentes avec des liens dynamiques et à jour."
        )

        # Générer le contenu du cours
        response = model.generate_content(prompt)
        generated_course = response.text
        html = markdown2.markdown(generated_course, extras=["fenced-code-blocks", "tables", "code-friendly"])
        
        # Enregistrer le cours dans la base de données
        new_cours = Document(title=title, content=html)
        new_cours.save()

        return render(
            request,
            "pages/cours/generate_cours.html",
            {"title": title, "generated_course": generated_course, "html_content": html},
        )

    # Afficher le formulaire si la méthode n'est pas POST
    return render(request, "pages/cours/generate_form.html")


# Créer un cours
def ajouter_cours(request):
    if request.method == "POST":
        form = CoursForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Cours ajouté avec succès.")
            return redirect("liste_cours")
    else:
        form = CoursForm()
    return render(request, "pages/cours/ajouter_cours.html", {"form": form})


# Modifier un cours
def modifier_cours(request, id):
    cours = get_object_or_404(Document, id=id)
    if request.method == "POST":
        form = CoursForm(request.POST, request.FILES, instance=cours)
        if form.is_valid():
            form.save()
            messages.success(request, "Cours modifié avec succès.")
            return redirect("details_cours", id=cours.id)
    else:
        form = CoursForm(instance=cours)
    return render(request, "pages/cours/modifier_cours.html", {"form": form, "cours": cours})


# Supprimer un cours
def supprimer_cours(request, id):
    cours = get_object_or_404(Document, id=id)
    if request.method == "POST":
        cours.delete()
        messages.success(request, "Cours supprimé avec succès.")
        return redirect("liste_cours")
    return render(request, "pages/cours/supprimer_cours.html", {"cours": cours})


# Afficher les détails d'un cours
# def details_cours(request, id):
#     cours = get_object_or_404(Document, id=id)
#     # Si vous voulez faire quelque chose si le fichier n'est pas présent
#     if not cours.fichier:
#         # Vous pouvez rediriger ou afficher un message approprié
#         return render(
#             request,
#             "pages/cours/details_cours.html",
#             {"cours": cours, "fichier_manquant": True},
#         )

#     return render(
#         request,
#         "pages/cours/details_cours.html",
#         {"cours": cours, "has_file": bool(cours.fichier)},
#     )
def details_cours(request, id):
    cours = get_object_or_404(Document, id=id)

    # Si le fichier n'est pas présent
    if not cours.fichier:
        return render(
            request,
            "pages/cours/details_cours.html",
            {"cours": cours, "fichier_manquant": True},
        )

    # Vérifier le type de fichier
    fichier_type = 'pdf' if cours.fichier.name.endswith('.pdf') else \
                   'image' if cours.fichier.name.endswith(('.jpg', '.png')) else \
                   'video' if cours.fichier.name.endswith('.mp4') else 'unknown'

    # Convertir le contenu en Markdown si nécessaire
    description_formattee = markdown2.markdown(cours.content)  # Assurez-vous que le champ 'description' existe

    return render(
        request,
        "pages/cours/details_cours.html",
        {
            "cours": cours,
            "has_file": bool(cours.fichier),
            "fichier_type": fichier_type,
           # "genere_par_ia": cours.genere_par_ia,  # Utilisez le bon nom de champ ici
            "description_formattee": description_formattee  # Ajoutez le contenu formaté
        },
    )


# Liste des cours
def liste_cours(request):
    query = request.GET.get("q")  # Récupérer la requête de recherche
    # Filtrer les cours par titre en fonction de la recherche
    if query:
        cours = Document.objects.filter(titre__icontains=query)
    else:
        cours = Document.objects.all()

    paginator = Paginator(
        cours, 10
    )  # Pagination: 10 cours par page (ajustez selon vos besoins)

    page_number = request.GET.get(
        "page"
    )  # Récupérer le numéro de page à partir de la requête
    page_obj = paginator.get_page(
        page_number
    )  # Obtenir les cours pour la page actuelle

    return render(
        request, "pages/cours/index.html", {"page_obj": page_obj, "query": query}
    )


def search_courses(request):
    query = request.GET.get("q", "")
    if query:
        cours = Document.objects.filter(title__icontains=query).values(
            "id", "title"
        )  # On récupère seulement les champs nécessaires
    else:
        cours = Document.objects.none()  # Si pas de recherche, renvoyer un queryset vide

    return JsonResponse(list(cours), safe=False)