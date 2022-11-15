import ratefile
import requests
import config
from urllib import parse
import json
from datetime import datetime
from flask import Flask, request    
from flask_cors import CORS
from flask import make_response

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
def user(summonerName):
    encodingSummonerName = parse.quote(summonerName)
    APIURL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodingSummonerName
    res = requests.get(APIURL, headers=headers)
    json_results["name"] = res.json()["name"]
    json_results["summonerName"] = res.json()["summonerLevel"]
    json_results["profileIconId"] = res.json()["profileIconId"]
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
        APIURL = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchId[i]
        res = requests.get(APIURL, headers=headers)
        data = res.json()
        win = 0
        for i in range(0,10) :
            if userpuuid== data["info"]["participants"][i]["puuid"] :
                win = i
                break
        gametime= datetime.fromtimestamp(data["info"]["gameStartTimestamp"] / 1000)

        if (gametime.month == 1):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["January"]["win"] +=1
            else :
                ratefile.monthrate["January"]["defeat"]+=1
        elif (gametime.month == 2):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["February"]["win"] +=1
            else :
                ratefile.monthrate["February"]["defeat"]+=1
        elif (gametime.month == 3):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["March"]["win"] +=1
            else :
                ratefile.monthrate["March"]["defeat"]+=1
        elif (gametime.month == 4):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["April"]["win"] +=1
            else :
                ratefile.monthrate["April"]["defeat"]+=1
        elif (gametime.month == 5):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["May"]["win"] +=1
            else :
                ratefile.monthrate["May"]["defeat"]+=1
        elif (gametime.month == 6):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["June"]["win"] +=1
            else :
                ratefile.monthrate["June"]["defeat"]+=1
        elif (gametime.month == 7):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["July"]["win"] +=1
            else :
                ratefile.monthrate["July"]["defeat"]+=1
        elif (gametime.month == 8):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["August"]["win"] +=1
            else :
                ratefile.monthrate["August"]["defeat"]+=1
        elif (gametime.month == 9):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["September"]["win"] +=1
            else :
                ratefile.monthrate["September"]["defeat"]+=1
        elif (gametime.month == 10):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["October"]["win"] +=1
            else :
                ratefile.monthrate["October"]["defeat"]+=1
        elif (gametime.month == 11):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["November"]["win"] +=1
            else :
                ratefile.monthrate["November"]["defeat"]+=1
        elif (gametime.month == 12):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["December"]["win"] +=1
            else :
                ratefile.monthrate["December"]["defeat"]+=1
        
        wincolection.append((data["info"]["participants"][win]["win"]))
    
    wincount =wincolection.count(True)
    defeatcount =wincolection.count(False)
    ratecount = (wincount/(wincount+defeatcount)*100)
    json_results["recent_rate"]= ratecount
    json_results["recent_win"] = wincount
    json_results["recent_defeat"] = defeatcount
    json_results["monthrate"] = ratefile.monthrate

@app.route('/monthsearch/<summonerName>', methods=['GET'])
def main(summonerName) :
    user(summonerName)
    monthinfo(userpuuid(summonerName))
    data_json= json.dumps(json_results,indent =3,ensure_ascii=False)
    print(data_json)
    res = make_response(data_json)
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Access-Control-Allow-Credentials"]="True"
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)