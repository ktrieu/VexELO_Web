import requests
import json
import dateutil.parser
import datetime
import collections
import grequests
from VexELO_rankings.models import Match, Team

class VexDbApi:

    MATCHES_URL = r'http://api.vexdb.io/v1/get_matches'
    EVENTS_URL = r'http://api.vexdb.io/v1/get_events'

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
        request_urls = list()
        for event_json in events_json:
            request_urls.append("{0}?sku={1}".format(self.MATCHES_URL, event_json['sku']))
        requests_list = [grequests.get(u) for u in request_urls]
        for idx, response in enumerate(grequests.map(requests_list, size=100, exception_handler=self.response_handler, stream=False)):
            event_json = events_json[idx]
            matches.extend(self.load_matches_from_event(response.json(), event_json['sku'], dateutil.parser.parse(event_json['start']), teams))
            response.close()
        return matches, teams

    def load_matches_from_event(self, matches_response, sku, start_date, team_dict):
        event_matches = matches_response['result']
        loaded_matches = list()
        #sort the matches into their order at the event
        event_matches.sort(key=lambda k: k['matchnum'])
        event_matches.sort(key=lambda k: k['instance'])
        event_matches.sort(key=lambda k: k['round'])
        for match in event_matches:
            if match['scored'] == '1':
                loaded_matches.append(self.parse_match_json(match, sku, start_date, team_dict))
        return loaded_matches

    def parse_match_json(self, json, sku, start_date, team_dict):
        #determine which teams are actually playing
        redTeams = [json['red1'], json['red2'], json['red3']]
        blueTeams = [json['blue1'], json['blue2'], json['blue3']]
        redTeams = [x for x in redTeams if x != json['redsit']]
        blueTeams = [x for x in blueTeams if x != json['bluesit']]
        #add teams in this match to the dict if they're not already there
        for team_name in redTeams + blueTeams:
            if team_name not in team_dict:
                team_dict[team_name] = Team(name=team_name, elo=1500)
        return Match(redTeam1=team_dict[redTeams[0]], redTeam2=team_dict[redTeams[1]],
                     blueTeam1=team_dict[blueTeams[0]], blueTeam2=team_dict[blueTeams[1]],
                     redScore=int(json['redscore']), blueScore=int(json['bluescore']), event_sku=sku, event_start_date=start_date)

    def response_handler(self, request, exception):
        print("Response exception.")
        print(exception)