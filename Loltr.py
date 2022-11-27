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
from collections import Counter

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": config.API_KEY
        }
json_results={}
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/')
def index():
    return "Hello it's your rate"


def user(summonerName):
    encodingSummonerName = parse.quote(summonerName)
    APIURL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + encodingSummonerName
    res = requests.get(APIURL, headers=headers)
    json_results["name"] = res.json()["name"]
    json_results["summonerLevel"] = res.json()["summonerLevel"]
    iconId= json.dumps(res.json()["profileIconId"])
    json_results["profileIconId"] ="http://ddragon.leagueoflegends.com/cdn/12.22.1/img/profileicon/"+iconId+".png"
    encrypted_id = res.json()['id']
    url_league = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"+ encrypted_id
    res_league = requests.get(url=url_league,headers=headers)
    json_results["tier"]= res_league.json()[0]["tier"]+" " +res_league.json()[0]["rank"]
    json_results["rank_wins"]= res_league.json()[0]["wins"]
    json_results["rank_losses"]= res_league.json()[0]["losses"]


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
    champlist=[]
    allitem=[]
    wincollection =[]
    wincount=0
    defeatcount=0
    for i in range(0,20):
      if matchId[i] in matchId:
        APIURL = "https://asia.api.riotgames.com/lol/match/v5/matches/" + matchId[i]
        res = requests.get(APIURL, headers=headers)
        data = res.json()
        player = 0
        itemlist=[]
        for i in range(0,10) :
            if userpuuid== data["metadata"]["participants"][i] :
                player = i
                break
        gametime= datetime.fromtimestamp(data["info"]["gameStartTimestamp"] / 1000)
        champlist.append(data["info"]["participants"][player]["championName"])
        itemlist.append(data["info"]["participants"][player]["item0"])
        itemlist.append(data["info"]["participants"][player]["item1"])
        itemlist.append(data["info"]["participants"][player]["item2"])
        itemlist.append(data["info"]["participants"][player]["item3"])
        itemlist.append(data["info"]["participants"][player]["item4"])
        itemlist.append(data["info"]["participants"][player]["item5"])
        itemlist.append(data["info"]["participants"][player]["item6"])
        remove_set={0,3111,2052,3158,3006,3020}
        itemlist=[i for i in itemlist if i not in remove_set]
        allitem.append(itemlist)
        if (gametime.month == 1):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["January"]["win"] +=1
            else :
                ratefile.monthrate["January"]["defeat"]+=1
        elif (gametime.month == 2):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["February"]["win"] +=1
            else :
                ratefile.monthrate["February"]["defeat"]+=1
        elif (gametime.month == 3):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["March"]["win"] +=1
            else :
                ratefile.monthrate["March"]["defeat"]+=1
        elif (gametime.month == 4):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["April"]["win"] +=1
            else :
                ratefile.monthrate["April"]["defeat"]+=1
        elif (gametime.month == 5):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["May"]["win"] +=1
            else :
                ratefile.monthrate["May"]["defeat"]+=1
        elif (gametime.month == 6):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["June"]["win"] +=1
            else :
                ratefile.monthrate["June"]["defeat"]+=1
        elif (gametime.month == 7):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["July"]["win"] +=1
            else :
                ratefile.monthrate["July"]["defeat"]+=1
        elif (gametime.month == 8):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["August"]["win"] +=1
            else :
                ratefile.monthrate["August"]["defeat"]+=1
        elif (gametime.month == 9):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["September"]["win"] +=1
            else :
                ratefile.monthrate["September"]["defeat"]+=1
        elif (gametime.month == 10):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["October"]["win"] +=1
            else :
                ratefile.monthrate["October"]["defeat"]+=1
        elif (gametime.month == 11):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["November"]["win"] +=1
            else :
                ratefile.monthrate["November"]["defeat"]+=1
        elif (gametime.month == 12):
            if data["info"]["participants"][player]["win"]==True :
                ratefile.monthrate["December"]["win"] +=1
            else :
                ratefile.monthrate["December"]["defeat"]+=1
        wincollection.append((data["info"]["participants"][player]["championName"],data["info"]["participants"][player]["win"],itemlist))
      else : print("key error")
    allitem=sum(allitem,[])
    mostchamp =Counter(champlist).most_common(n=3)
    mostitem= Counter(allitem).most_common(n=3)
    champ1=mostchamp[0][0]
    champ2=mostchamp[1][0]
    champ3=mostchamp[2][0]
    item1=str(mostitem[0][0])
    item2=str(mostitem[1][0])
    item3=str(mostitem[2][0])
    ratefile.mostchamp["champ1"]["name"]=champ1
    ratefile.mostchamp["champ2"]["name"]=champ2
    ratefile.mostchamp["champ3"]["name"]=champ3
    ratefile.mostchamp["champ1"]["link"]="https://ddragon.leagueoflegends.com/cdn/12.22.1/img/champion/"+champ1+".png"
    ratefile.mostchamp["champ2"]["link"]="https://ddragon.leagueoflegends.com/cdn/12.22.1/img/champion/"+champ2+".png"
    ratefile.mostchamp["champ3"]["link"]="https://ddragon.leagueoflegends.com/cdn/12.22.1/img/champion/"+champ3+".png"
    ratefile.mostitem["item1"]["code"]=item1
    ratefile.mostitem["item2"]["code"]=item2
    ratefile.mostitem["item3"]["code"]=item3
    ratefile.mostitem["item1"]["link"]="https://ddragon.leagueoflegends.com/cdn/12.22.1/img/item/"+item1+".png"
    ratefile.mostitem["item2"]["link"]="https://ddragon.leagueoflegends.com/cdn/12.22.1/img/item/"+item2+".png"
    ratefile.mostitem["item3"]["link"]="https://ddragon.leagueoflegends.com/cdn/12.22.1/img/item/"+item3+".png"
    for i in range(0,20) : 
        if wincollection[i][1] ==True :
            wincount+=1
        elif wincollection[i][1] ==False:
            defeatcount+=1
        if item1 in wincollection[i][2] :
            if wincollection[i][1]==True:
                ratefile.mostitem["item1"]["win"]+=1
            else :
                ratefile.mostitem["item1"]["defeat"]+=1
        elif item2 in wincollection[i][2] :
            if wincollection[i][1]==True:
                ratefile.mostitem["item2"]["win"]+=1
            else :
                ratefile.mostitem["item2"]["defeat"]+=1
        elif item3 in wincollection[i][2] :
            if wincollection[i][1]==True:
                ratefile.mostitem["item3"]["win"]+=1
            else :
                ratefile.mostitem["item3"]["defeat"]+=1
        if champ1 in wincollection[i][0] :
            if wincollection[i][1]==True:
                ratefile.mostchamp["champ1"]["win"]+=1
            else :
                ratefile.mostchamp["champ1"]["defeat"]+=1
        elif champ2 in wincollection[i][0] :
            if wincollection[i][1]==True:
                ratefile.mostchamp["champ2"]["win"]+=1
            else :
                ratefile.mostchamp["champ2"]["defeat"]+=1
        elif champ3 in wincollection[i][0] :
            if wincollection[i][1]==True:
                ratefile.mostchamp["champ3"]["win"]+=1
            else :
                ratefile.mostchamp["champ3"]["defeat"]+=1
    ratecount = (wincount/(wincount+defeatcount)*100)
    print(ratefile.mostitem)
    json_results["recent_rate"]= int(ratecount)
    json_results["recent_wins"] = wincount
    json_results["recent_losses"] = defeatcount
    json_results["monthrate"] = ratefile.monthrate
    json_results["mostchamp"] =ratefile.mostchamp
    json_results["mostitem"] =ratefile.mostitem

def monthclear(monthrate) :
    monthrate["January"]["win"]=0
    monthrate["January"]["defeat"]=0
    monthrate["February"]["win"]=0
    monthrate["February"]["defeat"]=0
    monthrate["March"]["win"]=0
    monthrate["March"]["defeat"]=0
    monthrate["April"]["win"]=0
    monthrate["April"]["defeat"]=0
    monthrate["May"]["win"]=0
    monthrate["May"]["defeat"]=0
    monthrate["June"]["win"]=0
    monthrate["June"]["defeat"]=0
    monthrate["July"]["win"]=0
    monthrate["July"]["defeat"]=0
    monthrate["August"]["win"]=0
    monthrate["August"]["defeat"]=0
    monthrate["September"]["win"]=0
    monthrate["September"]["defeat"]=0
    monthrate["October"]["win"]=0
    monthrate["October"]["defeat"]=0
    monthrate["November"]["win"]=0
    monthrate["November"]["defeat"]=0
    monthrate["December"]["win"]=0
    monthrate["December"]["defeat"]=0
    return monthrate

def mostchampclear(mostchamp) :
    mostchamp["champ1"]["win"]=0
    mostchamp["champ1"]["defeat"]=0
    mostchamp["champ2"]["win"]=0
    mostchamp["champ2"]["defeat"]=0
    mostchamp["champ3"]["win"]=0
    mostchamp["champ3"]["defeat"]=0
    return mostchamp

def mostitemclear(mostitem) :
    mostitem["item1"]["win"]=0
    mostitem["item1"]["defeat"]=0
    mostitem["item2"]["win"]=0
    mostitem["item2"]["defeat"]=0
    mostitem["item3"]["win"]=0
    mostitem["item3"]["defeat"]=0
    return mostitem

@app.route('/monthsearch/<summonerName>', methods=['GET'])
def main(summonerName) :
    user(summonerName)
    monthinfo(userpuuid(summonerName))
    res = make_response(json_results)
    monthclear(ratefile.monthrate)
    mostchampclear(ratefile.mostchamp)
    mostitemclear(ratefile.mostitem)
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Access-Control-Allow-Credentials"]="True"
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)