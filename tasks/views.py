from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer
from users.permissions import IsEmployer


class EmployerTaskListView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request):
        """List all tasks created by the logged-in employer."""
        if request.user.role != "EMPLOYER":
            return Response(
                {"error": "Only employers can view their tasks."},
                status=status.HTTP_403_FORBIDDEN,
            )

        tasks = Task.objects.filter(created_by=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployerCreateTaskView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def post(self, request):
        """Create a new task."""
        if request.user.role != "EMPLOYER":
            return Response(
                {"error": "Only employers can create tasks."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = TaskSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            task = serializer.save()
            return Response(
                {"message": "Task created successfully!", "task_id": task.id},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerUpdateTaskView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def put(self, request, task_id):
        """Update an existing task."""
        if request.user.role != "EMPLOYER":
            return Response(
                {"error": "Only employers can update tasks."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            task = Task.objects.get(id=task_id, created_by=request.user)
        except Task.DoesNotExist:
            return Response(
                {
                    "error": "Task not found or you are not authorized to edit this task."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Task updated successfully!"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerDeleteTaskView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def delete(self, request, task_id):
        """Delete a task."""
        if request.user.role != "EMPLOYER":
            return Response(
                {"error": "Only employers can delete tasks."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            task = Task.objects.get(id=task_id, created_by=request.user)
        except Task.DoesNotExist:
            return Response(
                {
                    "error": "Task not found or you are not authorized to delete this task."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        task.delete()
        return Response(
            {"message": "Task deleted successfully!"}, status=status.HTTP_200_OK
        )
