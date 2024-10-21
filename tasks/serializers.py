from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(
        source="created_by.phone_number"
    )  
    assigned_to = serializers.SlugRelatedField(
        slug_field="id",
        queryset=User.objects.filter(
            role="EMPLOYEE"
        ),  
        error_messages={
            "does_not_exist": "Employee with this phone number does not exist."
        },
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "created_by",
            "assigned_to",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_assigned_to(self, value):
        if value.role != "EMPLOYEE":
            raise serializers.ValidationError("Task can only be assigned to employees.")
        return value

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
