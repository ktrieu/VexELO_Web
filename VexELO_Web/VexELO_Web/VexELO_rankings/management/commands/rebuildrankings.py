from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic
from VexELO_rankings.rankings.vexdb import VexDbApi
from VexELO_rankings.models import Team, Match

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Rebuilding rankings...")
        self.stdout.write("Deleting existing tables...")
        Team.objects.all().delete()
        Match.objects.all().delete()
        vex_db_api = VexDbApi()
        self.stdout.write("Getting matches and teams...")
        matches = vex_db_api.get_all_matches()
        self.stdout.write("Inserting to database...")
        with atomic():
            for match in matches:
                redTeam1 = Team.objects.get_or_create(name=match.redTeam1, elo=1500)[0]
                redTeam2 = Team.objects.get_or_create(name=match.redTeam2, elo=1500)[0]
                blueTeam1 = Team.objects.get_or_create(name=match.blueTeam1, elo=1500)[0]
                blueTeam2 = Team.objects.get_or_create(name=match.blueTeam2, elo=1500)[0]
                Match.objects.create(redTeam1=redTeam1, redTeam2=redTeam2, blueTeam1=blueTeam1, blueTeam2=blueTeam2,
                                     redScore=match.redScore, blueScore=match.blueScore)
            


