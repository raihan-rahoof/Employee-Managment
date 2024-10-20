import re

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserRegistrationSerialiser(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                r"^[6-9]\d{9}$",
                "Phone number must be a valid Indian number starting with digits between 6 and 9, and it must be 10 digits long.",
            ),
            UniqueValidator(
                queryset=User.objects.all(), message="Phone number already in use"
            ),
        ],
    )
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("phone_number", "password", "role")

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long."
            )

        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )

        if not re.search(r"[@$!%*?&]", value):  # Add your desired special characters
            raise serializers.ValidationError(
                "Password must contain at least one special character (e.g., @$!%*?&)."
            )

        return value

    def create(self, validated_data):
        role = validated_data.get("role", "EMPLOYEE")
        if role == "EMPLOYER":
            return User.objects.create_employer(**validated_data)
        return User.objects.create_employee(**validated_data)
