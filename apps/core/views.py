from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok"})


# CLASS BASED VIEW
# from rest_framework.permissions import AlloAllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView


# class HealthCheckView(APIView):
#     permission_classes = [AlloAllowAny]

#     def get(self, request):
#         return Response({"status": "ok"})
