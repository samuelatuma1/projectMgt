from django.urls import path
from . import views
app_name = 'renthouse'
urlpatterns = [
    path("", views.index, name="index"),
    path("upload_house/", views.upload_house, name="upload_house"),
    path("sign_in/", views.sign_in, name="sign_in"),
    path("sign_in/<str:next_page>", views.sign_in, name="sign_in")
]

