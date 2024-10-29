import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Profile

from network.forms import ProfileForm

def index(request):
    if request.user.is_authenticated:
        return render(request, "network/index.html")
    
    else:
        return HttpResponseRedirect(reverse("network:login"))

@csrf_exempt
@login_required
def generate_post(request):
    #Composing a new post in the social media must be with a POST request
    if request.method != "POST":
        return JsonResponse({"error:" "POST request required."}, status=400)
    
    # Get content of the post
    data = json.loads(request.body)
    
    message = data.get("message", "")
    
    
    ...

def profile_regis(request):
    if request.method == 'POST':
        # Save the form data
        form  = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.username = request.user.username
            profile.birth_date = form.cleaned_data["birth_date"]
            profile.sex = form.cleaned_data["sex"]
            profile.save()
            return HttpResponseRedirect(reverse("network:index"))
    else: 
        form = ProfileForm()


def post(request, post_id):
    ...

def profile(request):
    user = request.user
    profile_form = ProfileForm()
    if not user.is_authenticated:
        return JsonResponse({"error": "Username not found or required."}, status=400)
    try:
        profile = user.rel_profile
    except Profile.DoesNotExist:
        return render(request, "network/profile_editor.html", {"username": user.username, "form": profile_form})
    
    return render(request, "network/profile.html", {"username": user.username, "profile": profile})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:profile"))
    else:
        return render(request, "network/register.html")

