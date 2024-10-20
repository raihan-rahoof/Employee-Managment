from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .managers import CustomBaseUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [("EMPLOYER", "Employer"), ("EMPLOYEE", "Employee"),("ADMIN","Admin")]
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="EMPLOYEE")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomBaseUserManager()

    def __str__(self):
        return f"{self.phone_number} - {self.role}"

    def clean(self):
        """Custom validation logic"""
        if self.role not in dict(self.ROLE_CHOICES):
            raise ValidationError(_("Invalid role for the user"))

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
