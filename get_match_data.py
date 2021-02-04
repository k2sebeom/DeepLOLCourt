import urllib.request as ur
from urllib.parse import quote
import json
from typing import List, Dict, Optional
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


with open('api_key.txt') as api_file:
    API_KEY = api_file.read().strip()
API_URL = 'https://kr.api.riotgames.com/lol'


def get_summoner_id(summoner_name: str) -> str:
    request_url = f'{API_URL}/summoner/v4/summoners/by-name/' \
                  f'{quote(summoner_name)}'
    request_url += f'?api_key={API_KEY}'
    with ur.urlopen(request_url) as f:
        resp = f.read().decode()
    summoner_data = json.loads(resp)
    return summoner_data['accountId']


def get_summoner_match_record(summoner_id: str) -> List[Dict]:
    request_url = f'{API_URL}/match/v4/matchlists/by-account/{summoner_id}'
    request_url += f'?api_key={API_KEY}'
    with ur.urlopen(request_url) as f:
        resp = f.read().decode()
    match_data = json.loads(resp)
    return match_data['matches']


def get_participant_id(match_id: int, summmoner_id: str) -> Optional[int]:
    request_url = f'{API_URL}/match/v4/matches/{match_id}'
    request_url += f'?api_key={API_KEY}'
    with ur.urlopen(request_url) as f:
        resp = f.read().decode()
    match_data = json.loads(resp)
    identities = match_data['participantIdentities']
    for identity_data in identities:
        if identity_data['player']['accountId'] == summoner_id:
            return identity_data['participantId']
    return None


def get_participants_from_match(match_id: int):
    request_url = f'{API_URL}/match/v4/matches/{match_id}'
    request_url += f'?api_key={API_KEY}'
    with ur.urlopen(request_url) as f:
        resp = f.read().decode()
    match_data = json.loads(resp)
    return match_data['participantIdentities']


def get_timeline_data(match_id: str):
    request_url = f'{API_URL}/match/v4/timelines/by-match/{match_id}'
    request_url += f'?api_key={API_KEY}'
    with ur.urlopen(request_url) as f:
        resp = f.read().decode()
    match_data = json.loads(resp)
    return match_data['frames'], match_data['frameInterval']


def track_participant_in_match(match_frames, participant_id, attribute,
                               interval=60000):
    t = []
    att = []
    for frame in match_frames:
        t.append(frame['timestamp'] / interval)
        att.append(frame['participantFrames'][str(participant_id)]['minionsKilled'] +
                   frame['participantFrames'][str(participant_id)]['jungleMinionsKilled'])
    return t, att


if __name__ == '__main__':
    font_path = '{path to your korean font}'
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()

    summoner_id = get_summoner_id('{summoner name}')
    matches = get_summoner_match_record(summoner_id)
    match_id = matches[1]["gameId"]
    participant_id = get_participant_id(match_id, summoner_id)
    frames, interval = get_timeline_data(match_id)
    players = get_participants_from_match(match_id)
    id_names = []
    for player in players:
        id_names.append(player['player']['summonerName'])
    for i in range(0, 5):
        t, cs = track_participant_in_match(frames, i + 1,
                                           "minionsKilled", interval=interval)
        plt.plot(t, cs, label=id_names[i])
    plt.legend(prop=font_prop)
    plt.xlabel('time (분)', fontproperties=font_prop)
    plt.ylabel('cs')
    plt.show()
