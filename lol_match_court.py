from client import RiotAPIClient
from data.match_dataset import MatchDataset
import numpy as np
import torch
from models.lol_result_model import LOLResultModel


with open('api_key.txt') as api_file:
    API_KEY = api_file.read().strip()

TEAM_KEYWORDS = ['riftHeraldKills', 'firstBlood', 'inhibitorKills',
                 'dragonKills', 'baronKills', 'win']
PLAYER_KEYWORDS = ['kills', 'deaths', 'assists', 'largestKillingSpree',
                   'largestMultiKill', 'totalDamageDealt',
                   'totalDamageDealtToChampions', 'totalHeal',
                   'damageSelfMitigated', 'goldEarned', 'goldSpent',
                   'inhibitorKills', 'totalMinionsKilled',
                   'neutralMinionsKilled', 'totalTimeCrowdControlDealt',
                   'champLevel', 'wardsPlaced', 'wardsKilled']


def get_summoner_name(match_data, participant_id):
    identities = match_data['participantIdentities']
    for p in identities:
        if p['participantId'] == participant_id:
            return p['player']['summonerName']
    return None


def get_match_feature(target_match, summoner_id):
    data = client.get_match_data(target_match['gameId'])

    player_participant_id = client.get_participant_id(target_match['gameId'],
                                                      summoner_id)
    if player_participant_id < 6:
        player_team = 100
    else:
        player_team = 200

    player_team_stat = []
    opponent_team_stat = []

    team_stat = data['teams']
    for team in team_stat:
        for team_key in TEAM_KEYWORDS:
            if team['teamId'] == player_team:
                player_team_stat.append(str(team[team_key]))
            else:
                opponent_team_stat.append(str(team[team_key]))

    player_participant_stat = []
    opponent_participant_stat = []
    participants = data['participants']
    for p in participants:
        if p['teamId'] == player_team:
            stat = player_participant_stat
        else:
            stat = opponent_participant_stat
        for part_key in PLAYER_KEYWORDS:
            stat.append(str(p['stats'][part_key]))

    data = ','.join(player_team_stat + player_participant_stat + \
                    opponent_team_stat + opponent_participant_stat)
    team_1, players_1, team_2, players_2 = MatchDataset.parse_data(data)
    team_1, result = MatchDataset.normalize_team_data(team_1)
    team_2, _ = MatchDataset.normalize_team_data(team_2)
    norm_1, norm_2 = MatchDataset.normalize_player_data(players_1, players_2)
    players_1 = np.concatenate(norm_1, 0)
    players_2 = np.concatenate(norm_2, 0)
    features = np.concatenate([team_1, players_1, team_2, players_2])
    return torch.tensor(features).unsqueeze(0).float()


if __name__ == '__main__':
    client = RiotAPIClient(wait=False)
    client.set_api_key(API_KEY)
    summoner_name = '백합의 향기'
    summoner_id = client.get_summoner_id(summoner_name)
    matches = client.get_summoner_match_record(summoner_id)

    target_match = matches[0]
    model = LOLResultModel(190)
    model.load_state_dict(torch.load('checkpoints/model.pth'))
    model.eval()

    x = get_match_feature(target_match, summoner_id)

    player_participant_id = client.get_participant_id(target_match['gameId'],
                                                      summoner_id)
    participants = [''] * 10
    data = client.get_match_data(target_match['gameId'])
    for j in range(10):
        i = data['participantIdentities'][j]['participantId'] - 1
        name = data['participantIdentities'][j]['player']['summonerName']
        participants[i] = name

    if player_participant_id < 6:
        participants = participants[:5]
    else:
        participants = participants[5:]

    with torch.no_grad():
        for p in range(1, 6):
            dist = []
            for i in range(5000):
                rand_x = x.clone().detach()
                rand_x[0][6 + (18 * (p - 1)):6 + (18 * p)] = torch.rand(18)
                output = model(rand_x)[0]
                pred = output.detach().cpu().numpy()[0]
                dist.append(pred)
            print(f"{participants[p - 1]} 가 없었다면 이길 확률: {np.mean(dist) * 100:.2f}%")
