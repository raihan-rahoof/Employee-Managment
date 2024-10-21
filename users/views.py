from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth import get_user_model

from .permissions import IsEmployer
from .serializers import EmployeerCreateSerializer,EmployeeSerializer

User = get_user_model()

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

class AdminCreateEmployerView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = EmployeerCreateSerializer(data=request.data)

        if serializer.is_valid():
            employer = serializer.save()
            return Response(
                {
                    "message": "Employer profile created successfully!",
                    "employer_id": employer.id,
                    "phone_number": employer.phone_number,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": "Employer creation failed", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class EmployerManageEmployeeView(APIView):
    permission_classes = [IsAuthenticated,IsEmployer]

    def post(self, request, *args, **kwargs):
        """Create a new employee."""
        user = request.user

        
        if user.role != "EMPLOYER":
            return Response(
                {"error": "Only employers can create employees."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                {
                    "message": "Employee created successfully!",
                    "employee_id": employee.id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, employee_id, *args, **kwargs):
        """Edit an existing employee."""
        user = request.user

        
        if user.role != "EMPLOYER":
            return Response(
                {"error": "Only employers can edit employees."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            employee = User.objects.get(id=employee_id, role="EMPLOYEE")
        except User.DoesNotExist:
            return Response(
                {"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Employee updated successfully!"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, employee_id, *args, **kwargs):
        """Delete an employee."""
        user = request.user

        
        if user.role != "EMPLOYER":
            return Response(
                {"error": "Only employers can delete employees."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            employee = User.objects.get(id=employee_id, role="EMPLOYEE")
        except User.DoesNotExist:
            return Response(
                {"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND
            )

        employee.delete()
        return Response(
            {"message": "Employee deleted successfully!"}, status=status.HTTP_200_OK
        )
