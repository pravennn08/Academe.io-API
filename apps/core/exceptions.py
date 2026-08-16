from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    errors = response.data

    if isinstance(exc, ValidationError):
        message = "Validation failed."
    else:
        message = {
            401: "Authentication is required.",
            403: "You do not have permission to perform this action.",
            404: "The requested resource was not found.",
            405: "This request method is not allowed.",
            429: "Too many requests. Please try again later.",
        }.get(response.status_code, "Request failed.")

    response.data = {
        "success": False,
        "status_code": response.status_code,
        "message": message,
        "errors": errors,
    }

    return response
