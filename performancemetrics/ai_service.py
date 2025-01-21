#import openai
#from django.conf import settings

#openai.api_key = settings.OPENAI_API_KEY
#def generate_recommendation(performance):
    #"""Generate a recommendation based on user performance data."""
   # prompt = (
       # f"Based on a user with an average score of {performance.average_score}, "
      #  f"tests taken: {performance.tests_taken}, "
     #   f"and last score of {performance.last_test_score}, "
      #  f"suggest improvement tips."
    #)
    
  #  response = openai.ChatCompletion.create(
      #  model="gpt-3.5-turbo",  # You can use "gpt-4" if you have access to it
     #   messages=[
       #     {"role": "user", "content": prompt}
     #   ],
   #     max_tokens=100
  #  )

  #  recommendation = response['choices'][0]['message']['content'].strip()
  #  return recommendation
    