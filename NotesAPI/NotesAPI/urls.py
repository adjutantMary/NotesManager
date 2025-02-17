from django.contrib import admin
from django.urls import include, path

# This code snippet is defining the URL patterns for a Django web application.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("notes.urls", namespace="authentication")),
]
