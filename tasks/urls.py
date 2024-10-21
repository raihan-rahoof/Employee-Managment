from django.urls import path
from .views import (
    EmployerTaskListView,
    EmployerCreateTaskView,
    EmployerUpdateTaskView,
    EmployerDeleteTaskView,
    EmployeeTaskView,
)

urlpatterns = [
    path("employer/tasks/", EmployerTaskListView.as_view(), name="task-list"),
    path("employer/task/create/", EmployerCreateTaskView.as_view(), name="create-task"),
    path(
        "employer/task/<int:task_id>/edit/",
        EmployerUpdateTaskView.as_view(),
        name="edit-task",
    ),
    path(
        "employer/task/<int:task_id>/delete/",
        EmployerDeleteTaskView.as_view(),
        name="delete-task",
    ),
    
    path('tasks/', EmployeeTaskView.as_view(), name='employee-task-list'),  
    path('tasks/<int:pk>/', EmployeeTaskView.as_view(), name='employee-task-update'),  

]
