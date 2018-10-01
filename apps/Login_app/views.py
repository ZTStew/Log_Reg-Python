from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages


def index(request):
	if "user_id" in request.session:
		return(redirect("/dashboard"))
	return render(request, "Login_app/index.html")

def register(request):
	results = User.objects.validate(request.POST)
	if not results[0]:
		for error_message in results[1]:
			messages.add_message(request, messages.ERROR, error_message)
	else:
		messages.add_message(request, messages.SUCCESS, 'You are Now Registered.', fail_silently = True)

	return(redirect("/"))

def login(request):
	results = User.objects.log(request.POST)

	if not results[0]:
		for error_message in results[1]:
			messages.add_message(request, messages.ERROR, error_message)
		return(redirect("/"))
	else:
		request.session["user_id"] = results[1].id
		return(redirect("/dashboard"))

def dashboard(request):
	if "user_id" not in request.session:
		return(redirect("/"))
	return render(request, "Login_app/dashboard.html")

def logout(request):
	request.session.clear()
	return redirect("/")

def users_api(request):
    users = User.objects.filter(first_name__startswith=request.POST['starts_with'])
    return render(request, 'Login_app/dashboard.html', { users: users })