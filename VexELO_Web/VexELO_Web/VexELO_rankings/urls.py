from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.rankings, name="rankings"),    
    url(r'^api/elo_data', views.elo_data, name='elo_data'),
    url(r'^api/predict_match', views.predict_match, name='predict_match'),
    url(r'^api/team_autocomplete', views.team_autocomplete, name='team_autocomplete'),
    url(r'^api/get_teams', views.get_teams, name='get_teams')
]