from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm, RegisterForm, QuestionForm, AnswerForm
from .models import Question, Answer
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'quora_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
        else:
            messages.error(request, "Login failed. See errors below.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'quora_app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'quora_app/post_question.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        questions = Question.objects.all().order_by('-created_at')
        return render(request, 'quora_app/dashboard.html', {'questions': questions})
    return render(request, 'quora_app/home.html')

@login_required
def answer_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('home')
    else:
        form = AnswerForm()
    return render(request, 'quora_app/answer_question.html', {'form': form, 'question': question})

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.user in answer.likes.all():
        messages.warning(request, "You already liked this answer.")
    else:
        answer.likes.add(request.user)
        messages.success(request, "You liked the answer.")
    return redirect('home')
