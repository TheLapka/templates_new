from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import Response

class LightView(GenericAPIView):
    def get(self, request):
        return Response("Hello word's /n I am first app")