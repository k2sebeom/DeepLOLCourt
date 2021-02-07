from client import RiotAPIClient
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


with open('api_key.txt') as api_file:
    API_KEY = api_file.read().strip()


if __name__ == '__main__':
    font_path = 'C:/Users/sebeo/AppData/Local/Microsoft/Windows/Fonts/NanumBarunGothic.ttf'

    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()

    client = RiotAPIClient()
    client.set_api_key(API_KEY)
    summoner_id = client.get_summoner_id('백합의 향기')
    matches = client.get_summoner_match_record(summoner_id)
    match_id = matches[0]["gameId"]
    participant_id = client.get_participant_id(match_id, summoner_id)
    frames, interval = client.get_timeline_data(match_id)
    players = client.get_participants_from_match(match_id)
    id_names = []
    for player in players:
        id_names.append(player['player']['summonerName'])
    for i in range(5) if participant_id < 5 else range(5, 10):
        t, cs = client.track_participant_in_match(frames, i + 1,
                                           "minionsKilled", interval=interval)
        plt.plot(t, cs, label=id_names[i])
    plt.legend(prop=font_prop)
    plt.xlabel('time (분)', fontproperties=font_prop)
    plt.ylabel('cs')
    plt.show()
