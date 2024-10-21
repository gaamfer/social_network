
from django.urls import path

from . import views

app_name="network"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("generate_post", views.generate_post, name="generate_post" ),
    path("post/<int:post_id>", views.post, name="post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("homepage/<str:username>", views.homepage, name="homepage")
]
