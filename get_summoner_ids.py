from client import RiotAPIClient
from tqdm import tqdm


with open('api_key.txt') as api_file:
    API_KEY = api_file.read().strip()


if __name__ == '__main__':
    client = RiotAPIClient()
    client.set_api_key(API_KEY)

    seed_name = '나다NADA'
    seed_id = client.get_summoner_id(seed_name)
    matches = client.get_summoner_match_record(seed_id)

    summoner_ids = set()
    for m in tqdm(matches):
        participants = client.get_participants_from_match(m['gameId'])
        for p in participants:
            summoner_ids.add(p['player']['accountId'] + '\n')
    with open('summoner_ids.txt', 'w') as id_file:
        id_file.writelines(summoner_ids)
