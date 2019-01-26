from django.shortcuts import render
from django.urls import path

# Create your views here.

class HomePageView(TemplateView):
    template_name = "index.html"
