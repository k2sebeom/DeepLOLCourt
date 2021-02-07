import urllib.request as ur
from urllib.parse import quote
import json
from typing import List, Dict, Optional
import time


class RiotAPIClient:
    def __init__(self):
        self.API_URL = 'https://kr.api.riotgames.com/lol'
        self.__API_KEY = ''

    def set_api_key(self, key):
        self.__API_KEY = key

    @property
    def api_key(self):
        return self.__API_KEY

    def use_riot_api(self, request_url):
        request_url = self.API_URL + request_url
        request_url += f'?api_key={self.api_key}'
        with ur.urlopen(request_url) as f:
            resp = f.read().decode()
        time.sleep(1.5)
        return json.loads(resp)

    def get_summoner_id(self, summoner_name: str) -> str:
        request_url = f'/summoner/v4/summoners/by-name/{quote(summoner_name)}'
        summoner_data = self.use_riot_api(request_url)
        return summoner_data['accountId']

    def get_summoner_match_record(self, summoner_id: str) -> List[Dict]:
        request_url = f'/match/v4/matchlists/by-account/{summoner_id}'
        match_data = self.use_riot_api(request_url)
        return match_data['matches']

    def get_match_data(self, match_id: int):
        request_url = f'/match/v4/matches/{match_id}'
        return self.use_riot_api(request_url)

    def get_participant_id(self, match_id: int, summoner_id: str) -> Optional[int]:
        request_url = f'/match/v4/matches/{match_id}'
        match_data = self.use_riot_api(request_url)
        identities = match_data['participantIdentities']
        for identity_data in identities:
            if identity_data['player']['accountId'] == summoner_id:
                return identity_data['participantId']
        return None

    def get_participants_from_match(self, match_id: int):
        request_url = f'/match/v4/matches/{match_id}'
        match_data = self.use_riot_api(request_url)
        return match_data['participantIdentities']

    def get_timeline_data(self, match_id: str):
        request_url = f'/match/v4/timelines/by-match/{match_id}'
        match_data = self.use_riot_api(request_url)
        return match_data['frames'], match_data['frameInterval']

    def track_participant_in_match(self, match_frames, participant_id,
                                   attribute, interval=60000):
        t = []
        att = []
        for frame in match_frames:
            t.append(frame['timestamp'] / interval)
            att.append(frame['participantFrames'][str(participant_id)]['minionsKilled'] +
                       frame['participantFrames'][str(participant_id)]['jungleMinionsKilled'])
        return t, att
