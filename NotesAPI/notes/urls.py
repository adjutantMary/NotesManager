from django.urls import path

from .views import (LoginAPIView, NoteCreateAPIView, NoteDeleteAPIView,
                    NoteListAPIView, NoteRetrieveUpdateAPIView,
                    RegistrationAPIView, UserRetrieveUpdateAPIView)

# This Python code snippet is defining URL patterns for a Django application. Here's a breakdown of
# what it does:
app_name = "authentication"
urlpatterns = [
    path("users/registration/", RegistrationAPIView.as_view()),
    path("user/update/", UserRetrieveUpdateAPIView.as_view()),
    path("users/login/", LoginAPIView.as_view()),
    path("notes/", NoteListAPIView.as_view()),
    path("notes/create/", NoteCreateAPIView.as_view()),
    path("notes/<int:pk>/", NoteRetrieveUpdateAPIView.as_view()),
    path("notes/<int:pk>/delete/", NoteDeleteAPIView.as_view()),
]
