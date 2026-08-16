from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from .permissions import IsAdministrator
from .serializers import (
    UserRegistrationResponseSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


class UserRegistrationAPIView(APIView):
    permission_classes = [IsAdministrator]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "user-registration"

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={
            201: UserRegistrationResponseSerializer,
        },
        summary="Create a user account",
        description="Creates a teacher, student, or parent account.",
        tags=["Users"],
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "success": True,
                "message": "User account created successfully.",
                "data": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )
