from django.urls import path
from . import views
urlpatterns = [

    path('', views.user_dashboard, name='user_dashboard'),
   # path('generate-recommendation/', views.generate_recommendation_view, name='generate_recommendation'),
    
    
]