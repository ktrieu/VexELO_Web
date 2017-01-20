from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import models
from VexELO_rankings.models import Match, Team
from VexELO_rankings.rankings import ranker

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

def predict_match(request):
    redTeam1 = Team.objects.get(name__iexact=request.GET['redTeam1'])
    redTeam2 = Team.objects.get(name__iexact=request.GET['redTeam2'])
    blueTeam1 = Team.objects.get(name__iexact=request.GET['blueTeam1'])
    blueTeam2 = Team.objects.get(name__iexact=request.GET['blueTeam2'])
    red_chance, blue_chance = ranker.predict_match(redTeam1.elo, redTeam2.elo, blueTeam1.elo, blueTeam2.elo)
    response_dict = dict()
    response_dict['status'] = 1
    response_dict['response'] = {'redProb': round(red_chance * 100, ndigits=2), 'blueProb': round(blue_chance * 100, ndigits=2)}
    return JsonResponse(response_dict)

def team_autocomplete(request):
    query = request.GET['query']
    results = [team.name for team in Team.objects.filter(name__istartswith=query)[:5]]
    return JsonResponse({'results': results})

def get_teams(request):
    teams = [team.name for team in Team.objects.all()]
    return JsonResponse({'teams' : teams})