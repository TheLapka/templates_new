from django.urls import path

from . import views

urlpatterns = [
    path("app_2/", view=views.LightView.as_view()),
]