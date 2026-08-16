from typing import Any

from auth_kit.authentication import JWTCookieAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.request import Request


class CSRFProtectedJWTCookieAuthentication(
    JWTCookieAuthentication,
):
    def authenticate(
        self,
        request: Request,
    ) -> tuple[Any, Any] | None:
        authorization_header = self.get_header(request)

        authenticated = super().authenticate(request)

        # CSRF is required only when authentication
        # came from the automatically sent JWT cookie.
        if authenticated is not None and authorization_header is None:
            SessionAuthentication().enforce_csrf(request)

        return authenticated
