from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Note, User


# The `RegistrationSerializer` class is used for serializing user registration data and creating a new
# user with email, username, and password fields.
class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя и создания нового."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "token"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# The `LoginSerializer` class in Python defines a serializer for user login data validation and
# authentication.
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )

        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")

        return {"email": user.email, "username": user.username, "token": user.token}


# The `UserSerializer` class in Python handles serialization and deserialization of User objects,
# including updating user information and password encryption.
class UserSerializer(serializers.ModelSerializer):
    """Ощуществляет сериализацию и десериализацию объектов User."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "token",
        )
        read_only_fields = ("token",)

    def update(self, instance, validated_data):
        """Выполняет обновление User."""

        password = validated_data.pop("password", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


# The `NoteSerializer` class is used for serializing note creation and updating operations in Python,
# with methods for creating and updating notes.
class NoteSerializer(serializers.ModelSerializer):
    """Сериализация создания и обновления заметки."""

    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        """Создание новой заметки."""
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Обновление существующей заметки."""
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance


# The `NoteDetailSerializer` class is used for serializing information about a note, including its
# title, content, creation date, and last update date.
class NoteDetailSerializer(serializers.ModelSerializer):
    """Сериализация для отображения информации о заметке."""

    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
