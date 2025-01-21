from django.urls import path


from . import views
from .views import  search_courses, liste_cours, generate_course



urlpatterns = [
 
   path('', liste_cours, name='liste_cours'),
    path('ajouter_cours/', views.ajouter_cours, name='ajouter_cours'),
    path('cours/<uuid:id>/modifier/', views.modifier_cours, name='modifier_cours'),
    path('cours/<uuid:id>/supprimer/', views.supprimer_cours, name='supprimer_cours'),
    path('cours/<uuid:id>/', views.details_cours, name='details_cours'),
  
    path('/search/', search_courses, name='search_courses'),
    path('cours/generate/', generate_course, name='generate_course'),
  
]


