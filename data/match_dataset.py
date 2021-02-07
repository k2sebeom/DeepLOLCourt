import numpy as np
from torch.utils.data import Dataset


class MatchDataset(Dataset):
    def __init__(self, dataroot):
        self.matches = []
        with open(dataroot, 'r', encoding='utf8') as match_file:
            self.matches = match_file.read().split('\n')[1:-1]

    def __len__(self):
        return len(self.matches)

    def __getitem__(self, idx):
        data = self.matches[idx]
        team_1, players_1, team_2, players_2 = self.parse_data(data)
        team_1, result = self.normalize_team_data(team_1)
        team_2, _ = self.normalize_team_data(team_2)
        norm_1, norm_2 = self.normalize_player_data(players_1, players_2)
        players_1 = np.concatenate(norm_1, 0)
        players_2 = np.concatenate(norm_2, 0)
        features = np.concatenate([team_1, players_1, team_2, players_2])
        return {'y': result, 'x': features.astype('float32')}

    def parse_data(self, data):
        row = data.split(',')
        blue_team = row[:6]
        blue_players = []
        for i in range(6, 6 + 18 * 5, 18):
            blue_players.append(row[i:i+18])
        red_team = row[96: 102]
        red_players = []
        for i in range(102, 102 + 18 * 5, 18):
            red_players.append(row[i:i+18])
        return np.array(blue_team), np.array(blue_players), \
               np.array(red_team), np.array(red_players)

    @staticmethod
    def normalize_team_data(team_data):
        normalized = np.zeros(team_data.shape)
        normalized[0] = float(team_data[0]) / 5.0
        normalized[1] = 1 if team_data[1] == 'TRUE' else 0
        normalized[2] = float(team_data[2]) / 20.0
        normalized[3] = float(team_data[3]) / 10.0
        normalized[4] = float(team_data[4]) / 10.0
        return normalized[:-1], 1 if team_data[5] == 'Win' else 0

    @staticmethod
    def normalize_player_data(players1, players2):
        normalized_1 = np.zeros(players1.shape)
        normalized_2 = np.zeros(players2.shape)
        all_players = np.concatenate([players1, players2], 0)
        for i in range(0, 18):
            max_val = np.max(all_players[:, i].astype('float32'))
            if max_val == 0:
                max_val = 1
            normalized_1[:, i] = players1[:, i].astype('float32') / max_val
            normalized_2[:, i] = players2[:, i].astype('float32') / max_val
        return normalized_1, normalized_2
