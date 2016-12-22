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
        #get a list of all matches and teams found
        matches, teams = vex_db_api.get_all_matches()
        self.stdout.write("Inserting to database...")
        #bulk insert all the teams into the database
        self.stdout.write("Inserting all teams...")
        Team.objects.bulk_create(teams.values())
        #read the teams back into memory to use them to create the matches
        db_teams_dict = dict()
        for db_team in Team.objects.all():
            db_teams_dict[db_team.name] = db_team
        #create all the matches
        db_matches = list()
        self.stdout.write("Inserting all matches...")
        for match in matches:
            db_matches.append(Match(redTeam1=db_teams_dict[match.redTeam1], redTeam2=db_teams_dict[match.redTeam2],
                                    blueTeam1=db_teams_dict[match.blueTeam1], blueTeam2=db_teams_dict[match.blueTeam2],
                                    redScore=match.redScore, blueScore=match.blueScore))
        Match.objects.bulk_create(db_matches)

              
    def save_match(self, match):
         redTeam1 = Team.objects.get_or_create(name=match.redTeam1, elo=1500)[0]
         redTeam2 = Team.objects.get_or_create(name=match.redTeam2, elo=1500)[0]
         blueTeam1 = Team.objects.get_or_create(name=match.blueTeam1, elo=1500)[0]
         blueTeam2 = Team.objects.get_or_create(name=match.blueTeam2, elo=1500)[0]
         Match.objects.create(redTeam1=redTeam1, redTeam2=redTeam2, blueTeam1=blueTeam1, blueTeam2=blueTeam2,
                              redScore=match.redScore, blueScore=match.blueScore)
            


