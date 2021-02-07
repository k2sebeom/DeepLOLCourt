from client import RiotAPIClient
from tqdm import tqdm

with open('api_key.txt') as api_file:
    API_KEY = api_file.read().strip()


TEAM_KEYWORDS = ['riftHeraldKills', 'firstBlood', 'inhibitorKills',
                 'dragonKills', 'baronKills']
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


if __name__ == '__main__':
    with open('summoner_ids.txt', 'r') as id_file:
        summoner_ids = id_file.read().split('\n')
    client = RiotAPIClient()
    client.set_api_key(API_KEY)

    data_file = open('match_data.csv', 'w', encoding='utf8')
    data_file.write(','.join(
        (TEAM_KEYWORDS + (['summonerName'] + PLAYER_KEYWORDS) * 5) * 2) + '\n'
    )
    print("Retrieving matches...")
    matches = []
    for s in tqdm(summoner_ids):
        matches += client.get_summoner_match_record(s)
    print("Processing match data...")
    for m in tqdm(matches):
        data = client.get_match_data(m['gameId'])
        blue_team_stat = []
        red_team_stat = []
        team_stat = data['teams']
        for team in team_stat:
            for team_key in TEAM_KEYWORDS:
                if team['teamId'] == 100:
                    blue_team_stat.append(str(team[team_key]))
                else:
                    red_team_stat.append(str(team[team_key]))

        blue_participant_stat = []
        red_participant_stat = []
        participants = data['participants']
        for p in participants:
            if p['teamId'] == 100:
                stat = blue_participant_stat
            else:
                stat = red_participant_stat
            stat.append(get_summoner_name(data, p['participantId']))
            for part_key in PLAYER_KEYWORDS:
                stat.append(str(p['stats'][part_key]))

        data_file.write(
            ','.join(
                blue_team_stat + blue_participant_stat +
                red_team_stat + red_participant_stat
            ) + '\n'
        )
    data_file.close()
