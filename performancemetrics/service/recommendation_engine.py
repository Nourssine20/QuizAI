

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from django.db.models import Avg
from performancemetrics.models import Performance , Recommendation
from quiz.models import Test





def load_performance_data(user_id=None):
    if user_id:
        performances = Performance.objects.filter(user_id=user_id).values('user_id').annotate(
            average_score=Avg('average_score'),
            last_test_score=Avg('last_test_score'),
            tests_taken=Avg('tests_taken')
        )
    else:
        performances = Performance.objects.values('user_id').annotate(
            average_score=Avg('average_score'),
            last_test_score=Avg('last_test_score'),
            tests_taken=Avg('tests_taken')
        )
    
    df = pd.DataFrame(performances)
    print("Performance Data Loaded:")
    print(df)  # Print the loaded performance data
    return df

def recommend_quizzes(user, num_recommendations=5):
    df = load_performance_data()

    if df.empty:
        print("No performance data available.")
        return []  

    # Check if there are at least two users to calculate similarity
    if len(df) < 2:
        print("Not enough data for recommendations. At least two users are required.")
        return []  

   
    scaler = StandardScaler()
    df[['average_score', 'last_test_score']] = scaler.fit_transform(df[['average_score', 'last_test_score']])
    
    print("Normalized Performance Data:")
    print(df[['user_id', 'average_score', 'last_test_score']])  # Print normalized data

  
    user_similarity = cosine_similarity(df[['average_score', 'last_test_score']])
    print("User Similarity Matrix:")
    print(user_similarity)  

    user_index = df.index[df['user_id'] == user.id]
    
    if user_index.empty:
        print(f"User {user.id} not found in performance data.")
        return []  # User not found in performance data

    user_index = user_index[0]
    similar_user_indices = user_similarity[user_index].argsort()[::-1][1:num_recommendations + 1]

    print("Similar User Indices:", similar_user_indices)  # Print indices of similar users

    recommended_quizzes = set()
    
    for similar_user_index in similar_user_indices:
        similar_user_id = df.iloc[similar_user_index]['user_id']
        user_tests = Test.objects.filter(taken_by=similar_user_id)

        # Check if the similar user performed well
        user_performance_queryset = Performance.objects.filter(user_id=similar_user_id)

        if user_performance_queryset.exists():
            # Calculate average performance for the similar user
            average_performance = user_performance_queryset.aggregate(
                average_score=Avg('average_score'),
                last_test_score=Avg('last_test_score')
            )
            
            print(f"User ID: {similar_user_id}, Average Performance: {average_performance}")  # Print average performance
            
            if average_performance['last_test_score'] > 0.8:  # Score > 80%
                for test in user_tests:
                    recommended_quizzes.add(test)

    print("Recommended Quizzes:", list(recommended_quizzes)[:num_recommendations])  # Print recommended quizzes
    return list(recommended_quizzes)[:num_recommendations]