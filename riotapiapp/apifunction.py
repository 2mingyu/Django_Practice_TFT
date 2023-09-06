import requests
from urllib import parse
import pprint
import math

pp = pprint.PrettyPrinter(indent=4)


def tft8_summoner_v1_summoners_by_name(request_header, summonerName):
    encodingSummonerName = parse.quote(summonerName)
    url = f"https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-name/{encodingSummonerName}"
    return requests.get(url, headers=request_header).json()


def tft8_league_v1_entries_by_summoner(request_header, summonerId):
    url = f"https://kr.api.riotgames.com/tft/league/v1/entries/by-summoner/{summonerId}"
    return requests.get(url, headers=request_header).json()


def tft8_match_v1_matches_by_puuid(request_header, puuid):
    url = f"https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=20"
    return requests.get(url, headers=request_header).json()


def tft8_match_v1_matches(request_header, matchId):
    url = f"https://asia.api.riotgames.com/tft/match/v1/matches/{matchId}"
    return requests.get(url, headers=request_header).json()


def myfunction(summonerName):
    request_header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": "RGAPI-b9113839-ef31-4c94-b4f5-0b89554e86c5"
    }

    myData = {}

    summoner_id_input = summonerName
    summoner_id_list = tft8_summoner_v1_summoners_by_name(request_header, summoner_id_input)
    summoner_profile = tft8_league_v1_entries_by_summoner(request_header, summoner_id_list['id'])
    summoner_profile = summoner_profile[0]
    matchIds = tft8_match_v1_matches_by_puuid(request_header, summoner_id_list['puuid'])

    print(
        f"{summoner_id_input}의 tier : {summoner_profile['tier']} {summoner_profile['rank']} {summoner_profile['leaguePoints']} points ")
    print(f"top4 횟수 : {summoner_profile['wins']}, 패배 횟수 : {summoner_profile['losses']}")
    myData['summonerName'] = summonerName
    myData['summonerLevel'] = summoner_id_list['summonerLevel']
    myData['tier'] = summoner_profile['tier']
    myData['winCount'] = summoner_profile['wins']
    myData['lossCount'] = summoner_profile['losses']
    myData['gameCount'] = myData['winCount'] + myData['lossCount']
    myData['winRate'] = myData['winCount'] / myData['gameCount'] * 100



    # 사용한 아이템, 특성, 유닛을 저장하는 dictionary
    summoner_using_units = {}
    summoner_using_traits = {}
    summoner_using_items = {}

    # 최근 최대 20개의 matchIds를 하나하나 순차하면서 사용한 아이템, 특성, 유닛들을 dictionary에 저장
    for matchId in matchIds:
        match_inform = tft8_match_v1_matches(request_header, matchId)

        # 하나의 match에서 사용자의 idx를 찾기 위한 반복문
        participants_idx = -1
        for idx in range(len(match_inform['metadata']['participants'])):
            if match_inform['metadata']['participants'][idx] == summoner_id_list['puuid']:
                participants_idx = idx
                break

        summoner_match_inform = match_inform['info']['participants'][participants_idx]
        win = False
        if summoner_match_inform['placement'] > 5:
            win = True
        tmp_win = 0
        if win:
            tmp_win = 1
            # match에서 사용한 아이템과 챔피언의 정보를 dictionary에 저장
        for unit in summoner_match_inform['units']:
            unit_name = unit['character_id']

            if not unit_name in summoner_using_units:
                summoner_using_units[unit_name] = (1, tmp_win)
            else:
                summoner_using_units[unit_name] = (summoner_using_units[unit_name][0]+1, summoner_using_units[unit_name][1] + tmp_win)

            for item in unit['items']:
                if not item in summoner_using_items:
                    summoner_using_items[item] = (1, tmp_win)
                else:
                    summoner_using_items[item] = (summoner_using_items[item][0] + 1, summoner_using_items[item][1] + tmp_win)

        # match에서 사용한 특성을 dictionary에 저장
        for trait in summoner_match_inform['traits']:
            trait_name = trait['name']
            if not trait_name in summoner_using_traits:
                summoner_using_traits[trait_name] = (1, tmp_win)
            else:
                summoner_using_traits[trait_name] = (summoner_using_traits[trait_name][0] + 1,summoner_using_traits[trait_name][1] +tmp_win)


    g = 3
    kk = summoner_using_units.items()
    summoner_using_units = sorted(summoner_using_units.items(), key= lambda item: item[1][0], reverse=True)
    summoner_using_traits = sorted(summoner_using_traits.items(), key= lambda item: item[1][0], reverse=True)
    summoner_using_items = sorted(summoner_using_items.items(), key= lambda item: item[1][0], reverse=True)

    traits = []
    for i in summoner_using_traits:
        trait = {'name': i[0], 'gameCount': i[1][0], 'winCount': i[1][1]}
        traits.append(trait)
    myData['traits'] = traits

    units = []
    for i in summoner_using_units:
        unit = {'name': i[0], 'gameCount': i[1][0], 'winCount': i[1][1]}
        units.append(unit)
    myData['units'] = units

    items = []
    for i in summoner_using_items:
        item = {'name': i[0], 'gameCount': i[1][0], 'winCount': i[1][1]}
        items.append(item)
    myData['items'] = items

    return myData


