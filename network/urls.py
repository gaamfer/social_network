from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name="network"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile_regis", views.profile_regis, name="profile_regis"),

    # API Routes
    path("generate_post", views.generate_post, name="generate_post" ),
    path("post/<int:post_id>", views.post, name="post"),
    path("profile/<str:username>", views.profile, name="profile")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)