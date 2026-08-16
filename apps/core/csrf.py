from django.http import JsonResponse


def csrf_failure(request, reason=""):
    return JsonResponse(
        {
            "success": False,
            "status_code": 403,
            "message": "CSRF verification failed.",
            "errors": {
                "detail": ("A valid CSRF token is required."),
            },
        },
        status=403,
    )
