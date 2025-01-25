from datetime import datetime, timedelta
from dateutil import tz
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import requests
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, CustomLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import FavoriteTeam as FT

api_key = "db5b6cfbea654c31bec2a7e34f994617"
headers = {
    "X-Auth-Token": api_key
}
params = {
        'limit': 500  # زيادة العدد لجلب المزيد من الفرق (حسب الدعم)
    }

leaguesCode = ["PD", "CL", "PL", "ELC", "DED", "SA", "FL1", "BL1", "WC"]
TreeOFLg = {
}
TreeOFTeams = {}
cleaned_teams_data = []
#get specific team data including all data regarding the team requested to be used for teamPage add them to TreeOfTeams
def getTeam(TeamID):
    global TreeOFTeams
    TreeOFTeams[TeamID] = {
        'info': requests.get(f"https://api.football-data.org/v4/teams/{TeamID}", headers=headers).json(),
        'matches':{'previous': [], 'future': [] },
        'squad': {
                "G":[],#GK
                "B":[],#backs
                "M":[],#middle
                "A":[],#attacks
                },
    }
    TreeOFTeams[TeamID]['coach'] = TreeOFTeams[TeamID]['info']['coach']
    for i in TreeOFTeams[TeamID]['info']['squad']:
        if i['position'] == 'Goalkeeper':
             TreeOFTeams[TeamID]['squad']['G'].append(i)
        elif i['position'] in ('Defence' , 'Left-Back' , 'Right-Back' , 'Centre-Back'):
             TreeOFTeams[TeamID]['squad']['B'].append(i) 
        elif i['position'] in ('Midfield', 'Offence', 'Central Midfield', 'Attacking Midfield', 'Defensive Midfield') :
            TreeOFTeams[TeamID]['squad']['M'].append(i) 
        else:
            TreeOFTeams[TeamID]['squad']['A'].append(i)  
    
    response = requests.get(f"https://api.football-data.org/v4/teams/{TeamID}/matches", headers=headers,params=params).json()
    x = list(response['matches'])
    
    for i in x: 
        utc_datetime = datetime.strptime(i['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
        utc_datetime = utc_datetime.replace(tzinfo=tz.UTC)
        local_datetime = utc_datetime.astimezone(tz.tzlocal())
        i['utcDate'] = local_datetime.strftime("%Y-%m-%d %I:%M %p")
        current_local_datetime = datetime.now(tz=tz.tzlocal())
        if current_local_datetime >= local_datetime:
            i['utcDate'] = local_datetime.strftime("%Y-%m-%d")
            TreeOFTeams[TeamID]['matches']['previous'].append(i)
        else:
                TreeOFTeams[TeamID]['matches']['future'].append(i)
    TreeOFTeams[TeamID]['matches']['previous'].reverse()
#filter data for all leagues to be used for our own API, this data are general data of team not detailed just to be used in user-friendly search
def getTeams(leagueCODE):
    global cleaned_teams_data
    global dirty_teams_data
    URL = f"http://api.football-data.org/v4/competitions/{leagueCODE}/teams"
    response = requests.get(URL, headers=headers,params=params)
    
    for x in response.json()['teams']:
        cleaned_teams_data.append({'id':x['id'], 'name':x['name'], 'shortname':x['shortName'], 'logo':x['crest']})
#fetch league needed data general data not specific such table is excluded add them to TreeOfLg
def indexData():
    global TreeOFLg
    global cleaned_teams_data
    global leaguesCode
    for i in leaguesCode:
        TreeOFLg[i] = {
            "matches": {"previous": [], "future":[]},
            "APIDATA":None,
            "scorers":None,
            "table":None,
            'indexData':None,
        }
    for key in TreeOFLg:
        TreeOFLg[key]['APIDATA'] =  requests.get(f"https://api.football-data.org/v4/competitions/{key}/standings", headers=headers).json()
        TreeOFLg[key]['indexData'] =  {
            "leaugeNAME":TreeOFLg[key]['APIDATA']['competition']['name'],
            "leaugeCODE" : TreeOFLg[key]['APIDATA']['competition']['code'],
            "leaugeID" : TreeOFLg[key]['APIDATA']['competition']['id'],
            "leaugeICON" : TreeOFLg[key]['APIDATA']['competition']['emblem']
        }
#get specific league data including all data regarding the league requested to be used for leaguePage (GET TABLE OF TEAM FOR THE LEAGUE) add them to TreeOfLg
def getLeagueInfo(leagueCode):
    global TreeOFLg
    toSet = []
    for y in TreeOFLg[leagueCode]['APIDATA']['standings'][0]['table']:
        toSet.append({
            'id':y['team']['id'],
            'position': y['position'],
            'team': y['team']['shortName'],
            'playedGames': y['playedGames'],
            'points' : y['points'],
             'goalDifference' : y['goalDifference']
        })
    TreeOFLg[leagueCode]['table'] = toSet
#get league matches add them to TreeOfLg
def getMatches(leagueCode):
        global TreeOFLg
        response = requests.get(f"https://api.football-data.org/v4/competitions/{leagueCode}/matches", headers=headers).json()
        x = list(response['matches'])

        for i in x: 
            utc_datetime = datetime.strptime(i['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
            utc_datetime = utc_datetime.replace(tzinfo=tz.UTC)
            local_datetime = utc_datetime.astimezone(tz.tzlocal())
            i['utcDate'] = local_datetime.strftime("%Y-%m-%d %I:%M %p")
            current_local_datetime = datetime.now(tz=tz.tzlocal())
            if current_local_datetime >= local_datetime:
                i['utcDate'] = local_datetime.strftime("%Y-%m-%d")
                TreeOFLg[leagueCode]['matches']['previous'].append(i)
            else:
                    TreeOFLg[leagueCode]['matches']['future'].append(i)
            TreeOFLg[leagueCode]['matches']['previous'].reverse()
#fetch league scorers add them to TreeOfLeg
def getScorers(leagueCode):
    global TreeOFLg
    TreeOFLg[leagueCode]['scorers'] = requests.get(f"https://api.football-data.org/v4/competitions/{leagueCode}/scorers", headers=headers).json()['scorers']

@login_required
def index(request):
    global TreeOFLg
    global TreeOFTeams
    #check did the user choose a team ?
    c = True
    favTeam = None
    if request.user.TeamID.TeamID is not None:
        if not TreeOFTeams: #this branch means TreeOFTeams is empty
            getTeam(request.user.TeamID.TeamID)
            favTeam = TreeOFTeams[request.user.TeamID.TeamID]  
        else:    
            for key in TreeOFTeams:
                if key == request.user.TeamID.TeamID:
                    c = False
                    break
            if c:
                getTeam(request.user.TeamID.TeamID)
            favTeam = TreeOFTeams[request.user.TeamID.TeamID]    
    if not TreeOFLg:
       indexData()
    #take for each league the needed data for the page index
    toSet = []
    for i in TreeOFLg:
        toSet.append(TreeOFLg[i]['indexData'])   
    return render(request, "status/index.html", {
        'data': toSet,
        'team':favTeam
    })

@login_required
def leaguePage(request, leagueCode):
    global TreeOFLg
    if TreeOFLg[leagueCode]['table'] == None:
        getLeagueInfo(leagueCode) #get The league table
    
    if len(TreeOFLg[leagueCode]['matches']['previous']) == 0:
        getMatches(leagueCode) #get The matches

    if TreeOFLg[leagueCode]['scorers'] == None:
        getScorers(leagueCode) #get The scorers
    
    return render(request, "status/leagueDetail.html", {
        'league': TreeOFLg[leagueCode]['APIDATA']['competition'],
        "table":TreeOFLg[leagueCode]['table'],
        'futureMatches':TreeOFLg[leagueCode]['matches']['future'],
        'previousMatches': TreeOFLg[leagueCode]['matches']['previous'],
        'scorers':TreeOFLg[leagueCode]['scorers']
    })

#user Authentication
class register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form':form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            FT(TeamID = form.cleaned_data['teamID'], user = User.objects.get(username=form.cleaned_data['username'])).save()
            return redirect('login')
        else:
            return render(request, 'registration/register.html', {'form':form})
        
class CustomLogin(LoginView):
    authentication_form = CustomLoginForm

#API for the teams, usually used for user-friedly search 
def teamsAPI(request):
    global cleaned_teams_data
    if len(cleaned_teams_data) == 0:
        for key in TreeOFLg:
            getTeams(key)
    return JsonResponse(cleaned_teams_data, safe=False)

#Team's info page
def teamPage(request, teamID):
    global TreeOFTeams
    c = True
    requestedTeam = None
    
    if not TreeOFTeams: #this branch means TreeOFTeams is empty
        getTeam(teamID)
        requestedTeam = TreeOFTeams[teamID]  
    else:    
        for key in TreeOFTeams:
            if key == teamID:
                c = False
                break
        if c:
            getTeam(teamID)
        requestedTeam = TreeOFTeams[teamID]    
    TreeOFLgKeys = list(TreeOFLg.keys())
    return render(request, "status/team.html", {#the following data u can find them in getTeam function
        'info': TreeOFTeams[teamID]['info'],
        'TreeOFLgKeys': TreeOFLgKeys,
        'squad':TreeOFTeams[teamID]['squad'],
        'coach': TreeOFTeams[teamID]['coach'],
        'matchesPerev':TreeOFTeams[teamID]['matches']['previous'],
        'matchesFuture':TreeOFTeams[teamID]['matches']['future'],
    })
    