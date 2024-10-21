from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserLoginView(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        user = authenticate(request, phone_number=phone_number, password=password)

        if not user:
            return Response(
                {"error": "Invalid phone number or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        if user.role == "ADMIN":
            dashboard_url = "/admin/dashboard/"
        elif user.role == "EMPLOYER":
            dashboard_url = "/employer/dashboard/"
        elif user.role == "EMPLOYEE":
            dashboard_url = "/employee/dashboard/"
        else:
            return Response(
                {"error": "User role is not recognized"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "phone_number": user.phone_number,
                    "role": user.role,
                    "dashboard_url": dashboard_url, 
                },
            },
            status=status.HTTP_200_OK,
        )
