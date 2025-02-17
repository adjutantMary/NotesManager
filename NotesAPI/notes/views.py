from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note, User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer,
    NoteDetailSerializer,
    NoteSerializer,
    RegistrationSerializer,
    UserSerializer,
)


# The `RegistrationAPIView` class is an API view in Python for user registration with permission
# settings, serializer, and response handling.
class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# This class represents a login API view in Python using Django REST framework.
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# This class defines API views for retrieving and updating user information with authentication and
# JSON rendering.
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get("user", {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("Data is updated")
        return Response(serializer.data, status=status.HTTP_200_OK)


# The `NoteCreateAPIView` class defines a view for creating a new note with the current authenticated
# user as the owner.
class NoteCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            # Устанавливаем текущего пользователя как владельца заметки
            note = serializer.save(user=request.user)
            return Response(
                NoteDetailSerializer(note).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# The `NoteListAPIView` class retrieves a list of notes belonging to the authenticated user and
# serializes them using `NoteDetailSerializer`.
class NoteListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        serializer = NoteDetailSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# This class defines API endpoints for retrieving and updating notes, with permission restrictions for
# authenticated users.
class NoteRetrieveUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk, user=self.request.user)
        except Note.DoesNotExist:
            return None

    def get(self, request, pk):
        note = self.get_object(pk)
        if note is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = NoteDetailSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk):
        note = self.get_object(pk)
        if note is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            updated_note = serializer.save()  # Обновляем заметку
            return Response(
                NoteDetailSerializer(updated_note).data
            )  # Возвращаем обновленные данные
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# The `NoteDeleteAPIView` class defines a view for deleting a specific note object associated with the
# authenticated user.
class NoteDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk, user=self.request.user)
        except Note.DoesNotExist:
            return None

    def delete(self, request, pk):
        note = self.get_object(pk)
        if note is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
