from match_dataset import MatchDataset
from torch.utils.data import DataLoader


if __name__ == '__main__':
    loader = DataLoader(MatchDataset(), 8, True)
    for i, data in enumerate(loader):
        print(data['x'].shape)

