from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import models
from VexELO_rankings.models import Match, Team

def index(request):
    return HttpResponse("Testing django website.")

def rankings(request):
    return render(request, "VexELO_rankings/rankings.html")

