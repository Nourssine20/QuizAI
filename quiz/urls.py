from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
   path('' , views.indexQuiz,  name='indexQuiz'),
   path('quiz/<uuid:quiz_id>/', views.quiz_detail, name='quiz_detail'),
   path('quiz/<uuid:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
  path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    
  
]
