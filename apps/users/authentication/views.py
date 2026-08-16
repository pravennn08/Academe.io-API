from auth_kit.views import (
    LoginView,
    RefreshViewWithCookieSupport,
)
from django.utils.decorators import (
    method_decorator,
)
from django.views.decorators.csrf import (
    csrf_protect,
    ensure_csrf_cookie,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


@method_decorator(
    ensure_csrf_cookie,
    name="dispatch",
)
class CSRFTokenAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = []

    def get(self, request):
        return Response(status=204)


@method_decorator(
    csrf_protect,
    name="dispatch",
)
class CSRFProtectedLoginView(LoginView):
    def create_response_with_cookies(
        self,
        serializer,
    ):
        response = super().create_response_with_cookies(serializer)

        # JWTs should only exist in HttpOnly cookies.
        if isinstance(response.data, dict):
            response.data.pop("access", None)
            response.data.pop("refresh", None)

        return response


@method_decorator(
    csrf_protect,
    name="dispatch",
)
class CSRFProtectedRefreshView(
    RefreshViewWithCookieSupport,
):
    def finalize_response(
        self,
        request,
        response,
        *args,
        **kwargs,
    ):
        response = super().finalize_response(
            request,
            response,
            *args,
            **kwargs,
        )

        # Prevent refreshed tokens from appearing
        # in the response body.
        if isinstance(response.data, dict):
            response.data.pop("access", None)
            response.data.pop("refresh", None)

        return response
