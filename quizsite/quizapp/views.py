from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth.decorators import login_required
from .models import Question, Result
from django.shortcuts import render, redirect
from django.db.models import Avg, Max, Min

@login_required
def my_results(request):
    results = Result.objects.filter(user=request.user).order_by('-timestamp')

    average = results.aggregate(Avg('score'))['score__avg'] or 0
    highest = results.aggregate(Max('score'))['score__max'] or 0
    lowest = results.aggregate(Min('score'))['score__min'] or 0

    return render(request, "quizapp/results_dashboard.html", {
        "results": results,
        "average": average,
        "highest": highest,
        "lowest": lowest
    })

@login_required
def start_quiz(request):
    # Get all questions from the database
    all_questions = list(Question.objects.all())

    # Select 5 random unique questions
    selected_questions = random.sample(all_questions, 5)

    # Save selected question IDs in session
    question_ids = [q.id for q in selected_questions]
    request.session['quiz_questions'] = question_ids
    request.session['current_q_index'] = 0
    request.session['user_answers'] = {}

    # Redirect to the first question handler
    return redirect('next-question')  # make sure 'next-question' is in urls.py
@login_required
def review_quiz(request):
    question_ids = request.session.get('quiz_questions', [])
    user_answers = request.session.get('user_answers', {})

    questions = Question.objects.filter(id__in=question_ids)

    if request.method == 'POST':
        # No need to update answers — just go submit
        return redirect('submit-quiz')

    return render(request, "quizapp/review.html", {
        "questions": questions,
        "user_answers": user_answers
    })

@login_required
def next_question(request):
    question_ids = request.session.get('quiz_questions')
    index = request.session.get('current_q_index', 0)

    # End quiz if all questions answered
    if index >= len(question_ids):
        return redirect('review-quiz')

    question = Question.objects.get(id=question_ids[index])

    if request.method == "POST":
        selected = request.POST.get(f'q{question.id}')
        user_answers = request.session.get('user_answers', {})
        user_answers[str(question.id)] = selected
        request.session['user_answers'] = user_answers
        request.session['current_q_index'] = index + 1
        return redirect('next-question')

    return render(request, "quizapp/quiz_single.html", {'question': question, 'index': index + 1})

@login_required
def submit_quiz(request):
    question_ids = request.session.get('quiz_questions', [])
    user_answers = request.session.get('user_answers', {})
    questions = Question.objects.filter(id__in=question_ids)

    score = 0
    for question in questions:
        selected = user_answers.get(str(question.id))
        if selected == question.correct_option:
            score += 1

    percentage = score * 20
    Result.objects.create(user=request.user, score=score, percentage=percentage)

    # Clear session
    request.session.pop('quiz_questions', None)
    request.session.pop('user_answers', None)
    request.session.pop('current_q_index', None)

    # Feedback
    if score <= 2:
        message = "Please try again!"
    elif score == 3:
        message = "Good job!"
    elif score == 4:
        message = "Excellent work!"
    else:
        message = "You are a genius!"

    return render(request, "quizapp/result.html", {
        "score": score,
        "percentage": percentage,
        "message": message
    })


@login_required
def quiz_home(request):
    return render(request, "quizapp/home.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "quizapp/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('quiz-home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "quizapp/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
