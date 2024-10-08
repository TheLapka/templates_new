from django.urls import path

from . import views

urlpatterns = [
    path("app_1/", view=views.LightView.as_view()),
]