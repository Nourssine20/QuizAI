from django.shortcuts import render, get_object_or_404
from .service.recommendation_engine import recommend_quizzes
from .models import Performance
#from .ai_service import generate_recommendation
from django.http import JsonResponse
from quiz.models import Test




# Create your views here.

def user_dashboard(request):
    user_id = request.user
    recommendations = recommend_quizzes(user_id)
    return render(request, 'pages/performance/index.html', {'recommendations': recommendations})
#@login_required
#def generate_recommendation_view(request):
    # Get all performances for the logged-in user
   # performances = Performance.objects.filter(user=request.user)

   # recommendations = []
   # quizzes = []

    # Generate recommendations and get associated quizzes for each performance
    #for performance in performances:
        # Generate recommendation for the current performance
       # recommendation_text = generate_recommendation(performance)
       # recommendation_data = {
          #  'performance_id': performance.id,
           # 'recommendation_text': recommendation_text,
           # 'average_score': performance.average_score,
           # 'tests_taken': performance.tests_taken,
           # 'last_test_score': performance.last_test_score
        #}
        #recommendations.append(recommendation_data)

        # Get all tests associated with the current performance
        #associated_quizzes = Test.objects.filter(performances=performance).values(
          #  'id', 'title', 'created_at', 'duration'
      #  )
       # quizzes.append({
        #    'performance_id': performance.id,
        #    'quizzes': list(associated_quizzes)  # Convert to list if needed for rendering
       # })

    # Render the recommendations and quizzes in the specified template
   # return render(request, 'pages/performance/recommendation.html', {
    #    'recommendations': recommendations,
      #  'quizzes': quizzes
   # })
