from django.urls import path

from .views import health_check

urlpatterns = [
    path("health/", health_check, name="health-check"),
]

# CLASS BASED URL
# from .views import HealthCheckView

# urlpatterns = [
#     path(
#         "health/",
#         HealthCheckView.as_view(),
#         name="health-check",
#     ),
# ]
