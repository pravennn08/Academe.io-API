from django.urls import include, path

from .views import (
    CSRFTokenAPIView,
)

app_name = "user-auth"

urlpatterns = [
    path(
        "csrf/",
        CSRFTokenAPIView.as_view(),
        name="csrf",
    ),
    path(
        "",
        include("auth_kit.urls"),
    ),
]
