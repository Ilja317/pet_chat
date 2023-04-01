from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as login_aut, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ChatRoomName

# Create your views here.

def register(request):
	if request.user.is_authenticated:
		redirect("home")
	form = UserCreationForm()
	if request.method == 'POST':
		username = request.POST["username"]
		username = username.lower()
		try:
			acc = User.objects.get(username=username)
			messages.error(request,"логин уже занят")
		except:
			form = UserCreationForm(request.POST)
			if form.is_valid():
				user = form.save(commit=False)
				user.username = user.username.lower()
				user.save()
				login_aut(request,user)
				return redirect("home")
			else:
				messages.error(request,"Логин или пароль не верен")
	return render(request, 'polsovatel/register.html', {'form': form})

def autorisation(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		if User.objects.filter(username=username.lower()).exists():
			user = authenticate(request,username=username,password=password)
			if user is not None :
				login_aut(request,user)
				return redirect("home")
			else:
				messages.error(request,"Логин или пароль введен не верно")
		else:
			messages.error(request, "Пользователь не зарегистрирован")


	return render(request,"polsovatel/enter.html")


def logout_user(request):
	if request.user.is_authenticated:
		logout(request)
		return redirect("home")
	return redirect("home")

@login_required(login_url="enter")
def home(request):
	if request.user.is_authenticated:
		users = User.objects.exclude(username=request.user.username)
	else :
		users = User.objects.all()
	container = {
		"users":users,
		"room": ChatRoomName.objects.get(owner=request.user).room
	}
	return render(request,"polsovatel/home.html",container)

def page_user(request,username):
	if User.objects.filter(username=username).exists:
		if username == request.user.username:
			return redirect("home")
		container = {
			"user" : User.objects.get(username=username),
			"room": "chat_%s" % ChatRoomName.objects.get(owner=request.user).room
		}
		return render(request,"polsovatel/page_user.html",container)
