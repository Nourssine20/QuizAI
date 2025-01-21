from django.urls import path
from . import views

urlpatterns = [
    path('generate_questions/', views.generate_questions, name='generate_questions'),
    path('save_question/', views.save_question, name='save_question'),
    path('export/questions/csv/', views.export_questions_csv, name='export_questions_csv'),
    path('export/questions/pdf/', views.export_questions_pdf, name='export_questions_pdf'),
]
