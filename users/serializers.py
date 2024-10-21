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
        fields = ("first_name","last_name","phone_number", "password", "role")

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

        if not re.search(r"[@$!%*?&]", value): 
            raise serializers.ValidationError(
                "Password must contain at least one special character (e.g., @$!%*?&)."
            )

        return value

    def create(self, validated_data):
        role = validated_data.get("role", "EMPLOYEE")
        if role == "EMPLOYER":
            return User.objects.create_employer(**validated_data)
        return User.objects.create_employee(**validated_data)


class EmployeerCreateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^[6-9]\d{9}$",
                message="Phone number must be a valid Indian number starting with digits between 6 and 9, and it must be 10 digits long.",
            ),
            UniqueValidator(
                queryset=User.objects.all(), message="Phone number is already in use."
            ),
        ],
    )
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "password", "role"]

    def validate_password(self,value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long."
            )
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not any(char.islower() for char in value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r"[@$!%*?&]", value):
            raise serializers.ValidationError(
                "Password must contain at least one special character (e.g., @$!%*?&)."
            )
        return value

    def create(self, validated_data):
        return User.objects.create_employer(**validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^[6-9]\d{9}$",
                message="Phone number must be a valid Indian number starting with digits between 6 and 9, and it must be 10 digits long.",
            ),
            UniqueValidator(
                queryset=User.objects.all(), message="Phone number already in use."
            ),
        ],
    )
    password = serializers.CharField(write_only=True, required=False, min_length=6)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "password"]

    def validate_password(self, value):
        if value:
            if len(value) < 6:
                raise serializers.ValidationError(
                    "Password must be at least 6 characters long."
                )
            if not any(char.isdigit() for char in value):
                raise serializers.ValidationError(
                    "Password must contain at least one digit."
                )
            if not any(char.isupper() for char in value):
                raise serializers.ValidationError(
                    "Password must contain at least one uppercase letter."
                )
            if not any(char.islower() for char in value):
                raise serializers.ValidationError(
                    "Password must contain at least one lowercase letter."
                )
            if not re.search(r"[@$!%*?&]", value):
                raise serializers.ValidationError(
                    "Password must contain at least one special character (e.g., @$!%*?&)."
                )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User.objects.create_employee(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance
