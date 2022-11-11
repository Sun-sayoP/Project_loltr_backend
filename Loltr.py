
import requests
import config
from urllib import parse
import json
from datetime import datetime
import time
from flask import Flask, render_template,request    
from flask_cors import CORS
from flask import make_response

app = Flask(__name__, template_folder="templates")
app.config['JSON_AS_ASCII'] = False
CORS(app)
monthrate = {
        "month": 
    {
      "January":  {
        "win":0,
        "defeat":0,
      },
      "February":  {
        "win":0,
        "defeat":0,
      },
      "March":  {
        "win":0,
        "defeat":0,
      },
      "April":  {
        "win":0,
        "defeat":0,
      },
      "May":  {
        "win":0,
        "defeat":0,
      },
      "June":  {
        "win":0,
        "defeat":0,
      },
      "July":  {
        "win":0,
        "defeat":0,
      },
      "August":  {
        "win":0,
        "defeat":0,
      },
      "September":  {
        "win":0,
        "defeat":0,
      },
      "October":  {
        "win":0,
        "defeat":0,
      },
      "November":  {
        "win":0,
        "defeat":0,
      },
      "December":  {
        "win":0,
        "defeat":0,
      }
    }
}
dayrate = {
        "day": 
    {
      "1st":  {
        "win":0,
        "defeat":0,
      },
      "2nd":  {
        "win":0,
        "defeat":0,
      },
      "3rd":  {
        "win":0,
        "defeat":0,
      },
      "4th":  {
        "win":0,
        "defeat":0,
      },
      "5th":  {
        "win":0,
        "defeat":0,
      },
      "6th":  {
        "win":0,
        "defeat":0,
      },
      "7th":  {
        "win":0,
        "defeat":0,
      },
      "8th":  {
        "win":0,
        "defeat":0,
      },
      "9th":  {
        "win":0,
        "defeat":0,
      },
      "10th":  {
        "win":0,
        "defeat":0,
      },
      "11th":  {
        "win":0,
        "defeat":0,
      },
      "12th":  {
        "win":0,
        "defeat":0,
      },
      "13th":  {
        "win":0,
        "defeat":0,
      },
      "14th":  {
        "win":0,
        "defeat":0,
      },
      "15th":  {
        "win":0,
        "defeat":0,
      },
      "16th":  {
        "win":0,
        "defeat":0,
      },
      "17th":  {
        "win":0,
        "defeat":0,
      },
      "18th":  {
        "win":0,
        "defeat":0,
      },
      "19th":  {
        "win":0,
        "defeat":0,
      },
      "20th":  {
        "win":0,
        "defeat":0,
      },
      "21th":  {
        "win":0,
        "defeat":0,
      },
      "22nd":  {
        "win":0,
        "defeat":0,
      },
      "23rd":  {
        "win":0,
        "defeat":0,
      },
      "24th":  {
        "win":0,
        "defeat":0,
      },
      "25th":  {
        "win":0,
        "defeat":0,
      },
      "26th":  {
        "win":0,
        "defeat":0,
      },
      "27th":  {
        "win":0,
        "defeat":0,
      },
      "28th":  {
        "win":0,
        "defeat":0,
      },
      "29th":  {
        "win":0,
        "defeat":0,
      },
      "30th":  {
        "win":0,
        "defeat":0,
      },
      "31st":  {
        "win":0,
        "defeat":0,
      }
    }
}
timerate = {
        "time": 
    {
      "0-3":  {
        "win":0,
        "defeat":0,
      },
      "3-6":  {
        "win":0,
        "defeat":0,
      },
      "6-9":  {
        "win":0,
        "defeat":0,
      },
      "9-12":  {
        "win":0,
        "defeat":0,
      },
      "12-15":  {
        "win":0,
        "defeat":0,
      },
      "15-18":  {
        "win":0,
        "defeat":0,
      },
      "18-21":  {
        "win":0,
        "defeat":0,
      },
      "21-24":  {
        "win":0,
        "defeat":0,
      }
    }
}
@app.route('/')
def index():
    return render_template('index.html')

def user(summonerName):
    encodingSummonerName = parse.quote(summonerName)
    APIURL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodingSummonerName
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": config.API_KEY
    }
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
    #return data["name"],data["summonerLevel"],data["profileIconId"]

def userpuuid(summonerName):
    encodingSummonerName = parse.quote(summonerName)
    APIURL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodingSummonerName
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": config.API_KEY
    }
    res = requests.get(APIURL, headers=headers)
    data = res.json()
    return data["puuid"]

def matches(summonerName) :
    encodingSummonerpuuid = userpuuid(summonerName)
    APIURL = "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" + encodingSummonerpuuid +"/ids?start=0&count=40"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": config.API_KEY
    }
    res = requests.get(APIURL, headers=headers)
    data = res.json()
    return data
def monthinfo(summonerName):
    matchId = matches (summonerName)
    checkpuuid =userpuuid(summonerName)    
    wincolection =[] 
    for i in range(0,40) :
        APIURL = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchId[i]
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": config.API_KEY
        }
        res = requests.get(APIURL, headers=headers)
        data = res.json()
        win = 0
        for i in range(0,10) :
            if checkpuuid== data["info"]["participants"][i]["puuid"] :
                win = i
                break
        gametime= datetime.fromtimestamp(data["info"]["gameStartTimestamp"] / 1000)

        if (gametime.month == 1):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["January"]["win"] +=1
            else :
                monthrate["month"]["January"]["defeat"]+=1
        if (gametime.month == 2):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["February"]["win"] +=1
            else :
                monthrate["month"]["February"]["defeat"]+=1
        if (gametime.month == 3):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["March"]["win"] +=1
            else :
                monthrate["month"]["March"]["defeat"]+=1
        if (gametime.month == 4):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["April"]["win"] +=1
            else :
                monthrate["month"]["April"]["defeat"]+=1
        if (gametime.month == 5):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["May"]["win"] +=1
            else :
                monthrate["month"]["May"]["defeat"]+=1
        if (gametime.month == 6):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["June"]["win"] +=1
            else :
                monthrate["month"]["June"]["defeat"]+=1
        if (gametime.month == 7):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["July"]["win"] +=1
            else :
                monthrate["month"]["July"]["defeat"]+=1
        if (gametime.month == 8):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["August"]["win"] +=1
            else :
                monthrate["month"]["August"]["defeat"]+=1
        if (gametime.month == 9):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["September"]["win"] +=1
            else :
                monthrate["month"]["September"]["defeat"]+=1
        if (gametime.month == 10):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["October"]["win"] +=1
            else :
                monthrate["month"]["October"]["defeat"]+=1
        if (gametime.month == 11):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["November"]["win"] +=1
            else :
                monthrate["month"]["November"]["defeat"]+=1
        if (gametime.month == 12):
            if data["info"]["participants"][win]["win"]==True :
                monthrate["month"]["December"]["win"] +=1
            else :
                monthrate["month"]["December"]["defeat"]+=1
        
        wincolection.append((data["info"]["participants"][win]["win"]))
    
    wincount =wincolection.count(True)
    defeatcount =wincolection.count(False)
    ratecount = (wincount/(wincount+defeatcount)*100)
    recent_rate = {
        "recent_rate": ratecount,
        "recent_win" : wincount, 
        "recent_defeat" : defeatcount
    }
    print(recent_rate)
    return monthrate,recent_rate

@app.route('/monthsearch/<summonerName>',methods=['GET'])
def main(summonerName) :
    #summonerName = request.args.get('name')
    data=[]
    print(data)
    data.append((user(summonerName),monthinfo(summonerName)))
    data_json= json.dumps(data,ensure_ascii=False)
    res = make_response(data_json)
    #length = len(data_json)
    #return render_template('test2.html',sum_name=summonerName,results=data_json,length=length)
    return res
