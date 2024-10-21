from django.urls import path
from .views import UserLoginView,AdminCreateEmployerView,EmployerManageEmployeeView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path(
        "myadmin/create-employer/",
        AdminCreateEmployerView.as_view(),
        name="admin-create-employer",
    ),
    path(
        "employer/employee/",
        EmployerManageEmployeeView.as_view(),
        name="manage-employee",
    ),  # for POST (create)
    path(
        "employer/employee/<int:employee_id>/",
        EmployerManageEmployeeView.as_view(),
        name="manage-employee",
    ),  # for PUT/DELETE (edit/delete)
]
