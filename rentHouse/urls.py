from django.urls import path
from . import views
app_name = 'renthouse'
urlpatterns = [
    path("", views.index, name="index"),
]

