from datetime import datetime, timedelta
from dateutil import tz
from django.shortcuts import render
from django.http import HttpResponse
import requests

api_key = "db5b6cfbea654c31bec2a7e34f994617"
headers = {
    "X-Auth-Token": api_key
}

TreeOFLg = {
    "PD": {"matches":{"previous":[],"future":[]},
    "APIDATA":None,
    "scorers":None,
    "table":None,
    'indexData':None,
    },
    "CL":{"matches":{"previous":[],"future":[]},
        "APIDATA":None,
        "scorers":None,
        "table":None,
        'indexData':None,
        },
    "PL":{"matches":{"previous":[],"future":[]},
        "APIDATA":None,
        "scorers":None,
        "table":None,
        'indexData':None,
    },
}

def indexData():
    for key in TreeOFLg:
        TreeOFLg[key]['APIDATA'] =  requests.get(f"https://api.football-data.org/v4/competitions/{key}/standings", headers=headers).json()
        TreeOFLg[key]['indexData'] =  {
            "leaugeNAME":TreeOFLg[key]['APIDATA']['competition']['name'],
            "leaugeCODE" : TreeOFLg[key]['APIDATA']['competition']['code'],
            "leaugeID" : TreeOFLg[key]['APIDATA']['competition']['id'],
            "leaugeICON" : TreeOFLg[key]['APIDATA']['competition']['emblem']
        }
 
def getLeagueInfo(leagueCode):
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

def setMatches(leagueCode):
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

def getScorers(leagueCode):
    TreeOFLg[leagueCode]['scorers'] = requests.get(f"https://api.football-data.org/v4/competitions/{leagueCode}/scorers", headers=headers).json()['scorers']

def index(request):
    if TreeOFLg['PD']['APIDATA'] == None:
       indexData()
    toSet = []
    for i in TreeOFLg:
        toSet.append(TreeOFLg[i]['indexData'])   
    return render(request, "status/index.html", {
        'data': toSet
    })

def leagueDetail(request, leagueCode):
    if TreeOFLg[leagueCode]['table'] == None:
        getLeagueInfo(leagueCode)
    
    if len(TreeOFLg[leagueCode]['matches']['previous']) == 0:
        setMatches(leagueCode)

    if TreeOFLg[leagueCode]['scorers'] == None:
        getScorers(leagueCode)
   
   
    return render(request, "status/leagueDetail.html", {
        'league': TreeOFLg[leagueCode]['APIDATA']['competition'],
        "table":TreeOFLg[leagueCode]['table'],
        'matches':TreeOFLg[leagueCode]['matches']['future'],
        'matchesF': TreeOFLg[leagueCode]['matches']['previous'],
        'scorers':TreeOFLg[leagueCode]['scorers']
    })
#Phase 1 end having index page and leagueDetail page 
#Phase 2 to include Team detail as it's pressable in the table of the league and matches and top score plyaer's team
#also we need to include pressable image in index page leading to page in which u can search for team and/or player
