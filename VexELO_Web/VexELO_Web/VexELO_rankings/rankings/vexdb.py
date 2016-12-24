import requests
import json
import dateutil.parser
from VexELO_rankings.models import Match, Team

class JsonMatch:

    redTeam1 = ""
    redTeam2 = ""
    blueTeam1 = ""
    blueTeam2 = ""

    redScore = 0
    blueScore = 0

    def __init__(self, redTeam1, redTeam2, blueTeam1, blueTeam2, redScore, blueScore):
        self.redTeam1 = redTeam1
        self.redTeam2 = redTeam2
        self.blueTeam1 = blueTeam1
        self.blueTeam2 = blueTeam2
        self.redScore = redScore
        self.blueScore = blueScore

class VexDbApi:

    MATCHES_URL = r'https://api.vexdb.io/v1/get_matches'
    EVENTS_URL = r'https://api.vexdb.io/v1/get_events'

    def get_matches_and_teams(self):
        #get the number of events
        nodata_response = requests.get(self.EVENTS_URL, {'season':'current', 'nodata':True, 'program':'VRC'}).json()
        num_events = nodata_response['size']
        #get every event
        count = 0
        events_json = list()
        while count < num_events:
            data_response = requests.get(self.EVENTS_URL, {'season':'current', 'program':'VRC'}).json()
            for event_json in data_response['result']:
                events_json.append(event_json)
            count += data_response['size']
        #sort the events based on date
        events_json.sort(key=lambda k: dateutil.parser.parse(k['start']))
        matches = list()
        teams = dict()
        for event_json in events_json:
            self.load_matches_from_event(event_json['sku'], matches, teams)
        return matches, teams

    def load_matches_from_event(self, sku, match_list, team_dict):
        matches_response = requests.get(self.MATCHES_URL, {'sku':sku}).json()
        event_matches = matches_response['result']
        #sort the matches into their order at the event
        event_matches.sort(key=lambda k: k['matchnum'])
        event_matches.sort(key=lambda k: k['instance'])
        event_matches.sort(key=lambda k: k['round'])
        for match in event_matches:
            if match['scored'] == '1':
                match_list.append(self.parse_match_json(match, team_dict))

    def parse_match_json(self, json, team_dict):
        #determine which teams are actually playing
        redTeams = [json['red1'], json['red2'], json['red3']]
        blueTeams = [json['blue1'], json['blue2'], json['blue3']]
        redTeams = [x for x in redTeams if x != json['redsit']]
        blueTeams = [x for x in blueTeams if x != json['bluesit']]
        #add teams in this match to the dict if they're not already there
        for team_name in redTeams + blueTeams:
            if team_name not in team_dict:
                team_dict[team_name] = Team(name=team_name, elo=1500)
        return JsonMatch(redTeams[0], redTeams[1], blueTeams[0], blueTeams[1], json['redscore'], json['bluescore'])
