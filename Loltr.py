import ratefile
import requests
import config
from urllib import parse
import json
from datetime import datetime
from flask import Flask, request    
from flask_cors import CORS
from flask import make_response
from collections import defaultdict

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return "Hello it's your rate"
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": config.API_KEY
        }
json_results={}
new_month=ratefile.monthrate
def user(summonerName):
    encodingSummonerName = parse.quote(summonerName)
    APIURL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodingSummonerName
    res = requests.get(APIURL, headers=headers)
    json_results["name"] = res.json()["name"]
    json_results["summonerLevel"] = res.json()["summonerLevel"]
    iconurl= json.dumps(res.json()["profileIconId"])
    json_results["profileIconId"] ="http://ddragon.leagueoflegends.com/cdn/12.21.1/img/profileicon/"+iconurl+".png"
    encrypted_id = res.json()['id']
    url_league = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+ encrypted_id
    res_league = requests.get(url=url_league,headers=headers)
    json_results["tier"]= res_league.json()[0]["tier"]
    json_results["rank"]= res_league.json()[0]["rank"]

def userpuuid(summonerName):
    encodingSummonerName = parse.quote(summonerName)
    APIURL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodingSummonerName
    res = requests.get(APIURL, headers=headers)
    data = res.json()
    return data["puuid"]

def matches(userpuuid) :
    APIURL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + userpuuid +"/ids?start=0&count=20"
    res = requests.get(APIURL, headers=headers)
    data = res.json()
    return data

def monthinfo(userpuuid):
    matchId = matches (userpuuid) 
    
    wincolection =[] 
    for i in range(0,20):
      if matchId[i] in matchId:
        APIURL = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchId[i]
        res = requests.get(APIURL, headers=headers)
        data = res.json()
        win = 0
        for i in range(0,10) :
            if userpuuid== data["info"]["participants"][i]["puuid"] :
                print(data["info"]["participants"][i]["puuid"])
                win = i
                break
        gametime= datetime.fromtimestamp(data["info"]["gameStartTimestamp"] / 1000)

        if (gametime.month == 1):
            if data["info"]["participants"][win]["win"]==True :
                new_month["January"]["win"] +=1
            else :
                new_month["January"]["defeat"]+=1
        elif (gametime.month == 2):
            if data["info"]["participants"][win]["win"]==True :
                new_month["February"]["win"] +=1
            else :
                new_month["February"]["defeat"]+=1
        elif (gametime.month == 3):
            if data["info"]["participants"][win]["win"]==True :
                new_month["March"]["win"] +=1
            else :
                new_month["March"]["defeat"]+=1
        elif (gametime.month == 4):
            if data["info"]["participants"][win]["win"]==True :
                new_month["April"]["win"] +=1
            else :
                new_month["April"]["defeat"]+=1
        elif (gametime.month == 5):
            if data["info"]["participants"][win]["win"]==True :
                new_month["May"]["win"] +=1
            else :
                new_month["May"]["defeat"]+=1
        elif (gametime.month == 6):
            if data["info"]["participants"][win]["win"]==True :
                new_month["June"]["win"] +=1
            else :
                new_month["June"]["defeat"]+=1
        elif (gametime.month == 7):
            if data["info"]["participants"][win]["win"]==True :
                new_month["July"]["win"] +=1
            else :
                new_month["July"]["defeat"]+=1
        elif (gametime.month == 8):
            if data["info"]["participants"][win]["win"]==True :
                new_month["August"]["win"] +=1
            else :
                new_month["August"]["defeat"]+=1
        elif (gametime.month == 9):
            if data["info"]["participants"][win]["win"]==True :
                new_month["September"]["win"] +=1
            else :
                new_month["September"]["defeat"]+=1
        elif (gametime.month == 10):
            if data["info"]["participants"][win]["win"]==True :
                new_month["October"]["win"] +=1
            else :
                new_month["October"]["defeat"]+=1
        elif (gametime.month == 11):
            if data["info"]["participants"][win]["win"]==True :
                new_month["November"]["win"] +=1
            else :
                new_month["November"]["defeat"]+=1
        elif (gametime.month == 12):
            if data["info"]["participants"][win]["win"]==True :
                new_month["December"]["win"] +=1
            else :
                new_month["December"]["defeat"]+=1
        
        wincolection.append((data["info"]["participants"][win]["win"]))
      else : print("key error ??")
    
    wincount =wincolection.count(True)
    defeatcount =wincolection.count(False)
    ratecount = (wincount/(wincount+defeatcount)*100)
    json_results["recent_rate"]= ratecount
    json_results["recent_win"] = wincount
    json_results["recent_defeat"] = defeatcount
    json_results["monthrate"] = new_month

@app.route('/monthsearch/<summonerName>', methods=['GET'])
def main(summonerName) :
    user(summonerName)
    monthinfo(userpuuid(summonerName))
    #data_json = json.dumps(json_results,ensure_ascii=False)
    #new_month.update({}.fromkeys(new_month, 0))
    res = make_response(json_results)
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Access-Control-Allow-Credentials"]="True"
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)