from django.shortcuts import render , get_object_or_404 , redirect
from django.utils import timezone
from django.contrib import messages
from .utils import generate_hint
from questions.models import Question


from .models import Test,Response,UserFeedback
from performancemetrics.models import Performance,Recommendation
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def indexQuiz(request):
    Quizzes = Test.objects.all()
    return render(request, 'pages/quiz/index.html', {'Quizzes': Quizzes})
# def quiz_detail(request, quiz_id):
#     quiz = get_object_or_404(Test, id=quiz_id)
#     shuffled_questions = quiz.questions.all().order_by('?')
#     for question in shuffled_questions:
#         question.generated_hint = generate_hint(question.content)
        
#     if request.method == "POST":
#         question_id = request.POST.get('question_id')
#         user_comment = request.POST.get('user_comment', '')
#         helpful = request.POST.get('helpful') == 'on'
#         feedback_id = request.POST.get('feedback_id', None)
#         # Ajouter ou mettre à jour le feedback de l'utilisateur
#         if feedback_id:  # Modification
#             feedback = UserFeedback.objects.get(id=feedback_id)
#             feedback.user_comment = user_comment
#             feedback.helpful = helpful
#             feedback.save()
#         else:  # Ajout
#             if question_id:
#                 question = Question.objects.get(id=question_id)
#                 UserFeedback.objects.create(question=question, user_comment=user_comment, helpful=helpful)

    
#     # Pass the duration of the quiz in seconds (e.g., 15 minutes * 60 = 900 seconds)
#     context = {
#         'quiz': quiz,
#         'questions': shuffled_questions,
#         'quiz_duration': quiz.duration * 60  # Convert duration to seconds if stored in minutes
#     }
#     return render(request, 'pages/quiz/quiz_detail.html', context)
@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Test, id=quiz_id)
    shuffled_questions = quiz.questions.all().order_by('?')
    
    # Generate hints for each question on initial load
    for question in shuffled_questions:
        question.generated_hint = generate_hint(question.content)
    
    # AJAX request to get a new hint for a specific question without reloading the page
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        question_id = request.POST.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        new_hint = generate_hint(question.content)
        return JsonResponse({'new_hint': new_hint})

    # If not an AJAX request, load the entire quiz page normally
    context = {
        'quiz': quiz,
        'questions': shuffled_questions,
        'quiz_duration': quiz.duration * 60  # Convert duration to seconds if stored in minutes
    }
    return render(request, 'pages/quiz/quiz_detail.html', context)
@login_required

def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Test, id=quiz_id)
    questions = quiz.questions.all()
    total_questions = questions.count()
    correct_answers = 0

    if request.method == "POST":
        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
           
           
            if selected_answer_id:
                if question.question_type == 'true_false':
                    # Check true/false responses
                    correct_response = question.responses.filter(is_correct=True).first()
                   
                    # Ensure correct_response is not None
                    if correct_response:
                        if (selected_answer_id == 'true' and correct_response.response_content == 'vrai') or \
                           (selected_answer_id == 'false' and correct_response.response_content == 'faux'):
                            correct_answers += 1
                elif question.question_type == 'choice':
                    # For multiple choice, validate answer as a UUID
                    try:
                        selected_answer = get_object_or_404(Response, id=selected_answer_id)
                        if selected_answer.is_correct:
                            correct_answers += 1
                    except ValueError:
                        continue  # Skip if the selected answer is not a valid UUID
                elif question.question_type == 'open':
                    # Placeholder for open-ended questions
                    # Could add logic to evaluate if answers are programmatically scored
                    pass

        # Calculate score as a percentage
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        performance = Performance.objects.create(
            user=request.user,
            test=quiz,
            tests_taken=1,
            last_test_score=score,
            average_score=score  # Start average_score as the current score
        )
        if score < 50:
            recommendation_content = "Consider reviewing the material thoroughly and try again."
        elif score < 80:
            recommendation_content = "Good effort! A bit more practice might help improve your score."
        else:
            recommendation_content = "Excellent work! Keep up the great results."

        # Save the recommendation associated with the performance
        Recommendation.objects.create(content=recommendation_content, performance=performance)
        findPerformance=Performance.objects.filter(user=request.user,test=quiz)
        total_score = sum(p.last_test_score for p in findPerformance)
        total_tests_taken = findPerformance.count()
       
        average_score = total_score / total_tests_taken if total_tests_taken > 0 else 0

        # Optionally, show a success message or redirect
        messages.success(request, f"You scored {score}%!")
        
        # Redirect to a results page or render it
        return render(request, 'pages/quiz/quiz_results.html', {
            'quiz': quiz,
            'score': score,
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'performance': {
            'average_score': average_score,
            'count': total_tests_taken,
            'last_test_score': findPerformance.last().last_test_score if findPerformance.exists() else 0,
               },
            'recommendation': recommendation_content,
        })
    
    # If GET request, redirect back to the quiz page
    return redirect('quiz_detail', quiz_id=quiz.id)
@require_POST
@login_required
def submit_feedback(request):
    question_id = request.POST.get('question_id')
    user_comment = request.POST.get('user_comment', '')
    helpful = request.POST.get('helpful', 'false') == 'true'
    
    question = Question.objects.get(id=question_id)
    feedback = UserFeedback.objects.create(
        question=question,
        user_comment=user_comment,
        helpful=helpful
    )
    return JsonResponse({'status': 'success'})