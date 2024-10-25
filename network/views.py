import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User


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

def post(request, post_id):
    ...

def profile(request, username):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    return render(request, "network/profile.html", {"username": username})
    ...


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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")

