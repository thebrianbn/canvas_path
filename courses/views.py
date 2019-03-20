from django.shortcuts import render
from django.urls import path
from django.views import View


class Home(View):

    def get(self, request):
        return render(request, "home.html")
