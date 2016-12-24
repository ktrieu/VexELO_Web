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
        matches, teams = vex_db_api.get_matches_and_teams()
        self.stdout.write("Writing teams to database...")
        Team.objects.bulk_create(teams.values())
        self.stdout.write("Writing matches to database...")
        db_teams = dict()
        db_matches = list()
        for team in Team.objects.all():
            db_teams[team.name] = team
        for idx, match in enumerate(matches):
            db_matches.append(Match(redTeam1=db_teams[match.redTeam1], redTeam2=db_teams[match.redTeam2],
                                    blueTeam1=db_teams[match.blueTeam1], blueTeam2=db_teams[match.blueTeam2],
                                    redScore=match.redScore, blueScore=match.blueScore, match_num=idx))
        Match.objects.bulk_create(db_matches)

             
            


