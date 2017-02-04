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
        self.stdout.write(len(teams.values())
        self.stdout.write(teams.values())
        #rank teams for each match
        self.stdout.write("Ranking matches...")
        for match in matches:
            ranker.rank_match(match, teams)
        self.stdout.write("Writing teams to database...")
        Team.objects.bulk_create(teams.values())
        #reload team models to get the primary keys back
        db_teams = dict()
        db_teams = {team.name : team for team in Team.objects.all()}
        self.stdout.write("Writing matches to database...")
        for idx, match in enumerate(matches):
            match.redTeam1 = db_teams[match.redTeam1.name]
            match.redTeam2 = db_teams[match.redTeam2.name]
            match.blueTeam1 = db_teams[match.blueTeam1.name]
            match.blueTeam2 = db_teams[match.blueTeam2.name]
            match.match_num = idx
        #Match.objects.bulk_create(matches)
             
            


