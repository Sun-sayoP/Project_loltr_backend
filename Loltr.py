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
def user(summonerName):
    encodingSummonerName = parse.quote(summonerName)
    APIURL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodingSummonerName
    results = []
    res = requests.get(APIURL, headers=headers)
    results.append(res.json()["name"])
    results.append(res.json()["summonerLevel"])
    results.append(res.json()["profileIconId"])
    encrypted_id = res.json()['id']
    url_league = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{}".format(encrypted_id)
    res_league = requests.get(url=url_league,headers=headers)
    league_dicts = res_league.json()
    def get_league_info(league_dict):
        res = [
        league_dict.get('tier'),
        league_dict.get('rank'),
            ]
        return res
    
    for league_dict in league_dicts:
        results.append(get_league_info(league_dict))
    
    print(results)
    return results

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

def monthinfo(summonerName,userpuuid):
    matchId = matches (userpuuid)
    print(matchId)   
    wincolection =[] 
    for i in range(0,20):
        APIURL = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchId[i]
        res = requests.get(APIURL, headers=headers)
        data = res.json()
        win = 0
        if data["info"] in data :
          try:
            print(data["info"])
          except:
            print("error")
        for i in range(0,10) :
            if userpuuid== data["info"]["participants"][i]["puuid"] :
                win = i
                break
        gametime= datetime.fromtimestamp(data["info"]["gameStartTimestamp"] / 1000)

        if (gametime.month == 1):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["January"]["win"] +=1
            else :
                ratefile.monthrate["month"]["January"]["defeat"]+=1
        elif (gametime.month == 2):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["February"]["win"] +=1
            else :
                ratefile.monthrate["month"]["February"]["defeat"]+=1
        elif (gametime.month == 3):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["March"]["win"] +=1
            else :
                ratefile.monthrate["month"]["March"]["defeat"]+=1
        elif (gametime.month == 4):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["April"]["win"] +=1
            else :
                ratefile.monthrate["month"]["April"]["defeat"]+=1
        elif (gametime.month == 5):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["May"]["win"] +=1
            else :
                ratefile.monthrate["month"]["May"]["defeat"]+=1
        elif (gametime.month == 6):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["June"]["win"] +=1
            else :
                ratefile.monthrate["month"]["June"]["defeat"]+=1
        elif (gametime.month == 7):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["July"]["win"] +=1
            else :
                ratefile.monthrate["month"]["July"]["defeat"]+=1
        elif (gametime.month == 8):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["August"]["win"] +=1
            else :
                ratefile.monthrate["month"]["August"]["defeat"]+=1
        elif (gametime.month == 9):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["September"]["win"] +=1
            else :
                ratefile.monthrate["month"]["September"]["defeat"]+=1
        elif (gametime.month == 10):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["October"]["win"] +=1
            else :
                ratefile.monthrate["month"]["October"]["defeat"]+=1
        elif (gametime.month == 11):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["November"]["win"] +=1
            else :
                ratefile.monthrate["month"]["November"]["defeat"]+=1
        elif (gametime.month == 12):
            if data["info"]["participants"][win]["win"]==True :
                ratefile.monthrate["month"]["December"]["win"] +=1
            else :
                ratefile.monthrate["month"]["December"]["defeat"]+=1
        
        wincolection.append((data["info"]["participants"][win]["win"]))
    
    wincount =wincolection.count(True)
    defeatcount =wincolection.count(False)
    ratecount = (wincount/(wincount+defeatcount)*100)
    recent_rate = {
        "recent_rate": ratecount,
        "recent_win" : wincount, 
        "recent_defeat" : defeatcount
    }
    return ratefile.monthrate,recent_rate

@app.route('/monthsearch/<summonerName>',methods=['GET'])
def main(summonerName) :
    data=[]
    data.append(user(summonerName))
    data.append(monthinfo(summonerName,userpuuid(summonerName)))
    data_json= json.dumps(data,ensure_ascii=False)
    res = make_response(data_json)
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Access-Control-Allow-Credentials"]="True"
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)