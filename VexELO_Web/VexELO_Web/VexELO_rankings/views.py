from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import models
from VexELO_rankings.models import Match, Team

def index(request):
    return HttpResponse("Testing django website.")

def rankings(request):
    return render(request, "VexELO_rankings/rankings.html")

def elo_data(request):
    all_teams = Team.objects.all()
    response_dict = {}
    response_dict['data'] = list()
    for idx, team in enumerate(all_teams):
        response_dict['data'].append(dict({'name':team.name, 'elo':int(round(team.elo))})) 
    return JsonResponse(response_dict)
