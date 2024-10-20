from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomBaseUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_("Phone number must be set"))

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_employer(self, phone_number, password=None, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", "EMPLOYER")

        return self.create_user(phone_number, password, **extra_fields)

    def create_employee(self, phone_number, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", "EMPLOYEE")

        return self.create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")  # Or any role you want for superuser

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(phone_number, password, **extra_fields)
