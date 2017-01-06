from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic
from VexELO_rankings.rankings.vexdb import VexDbApi
from VexELO_rankings.models import Team, Match
from VexELO_rankings.rankings import ranker

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Rebuilding rankings...")
        self.stdout.write("Deleting existing tables...")
        Team.objects.all().delete()
        Match.objects.all().delete()
        vex_db_api = VexDbApi()
        self.stdout.write("Getting matches and teams...")
        matches, teams = vex_db_api.get_matches_and_teams()
        #rank teams for each match
        self.stdout.write("Ranking matches...")
        for match in matches:
            ranker.rank_match(match, teams)
        self.stdout.write("Writing teams to database...")
        team_models = list()
        team_models = [Team(name=team.name, elo=team.elo) for team in teams.values()]
        Team.objects.bulk_create(team_models)
        #reload team models to get the primary keys back
        db_teams = dict()
        db_teams = {team.name : team for team in Team.objects.all()}
        self.stdout.write("Writing matches to database...")
        match_models = [Match(redTeam1=db_teams[match.redTeam1], redTeam2=db_teams[match.redTeam2], blueTeam1=db_teams[match.blueTeam1],
                              blueTeam2=db_teams[match.blueTeam2], redScore=match.redScore, blueScore=match.blueScore, match_num = idx)
                        for idx, match in enumerate(matches)]
        Match.objects.bulk_create(match_models)
             
            


