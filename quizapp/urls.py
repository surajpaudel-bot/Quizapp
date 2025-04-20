from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.login_view, name='home'),  # this makes "home" point to login view for now
    path('home/', views.quiz_home, name='quiz-home'),
    path('quiz/', views.start_quiz, name='start-quiz'),
    path('quiz/submit/', views.submit_quiz, name='submit-quiz'),
    path('my-results/', views.my_results, name='my-results'),
    path('quiz/next/', views.next_question, name='next-question'),
    path('quiz/review/', views.review_quiz, name='review-quiz'),
]
