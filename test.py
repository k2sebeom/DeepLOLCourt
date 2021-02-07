from data.match_dataset import MatchDataset
from torch.utils.data import DataLoader
from models.lol_result_model import LOLResultModel
import torch


if __name__ == '__main__':
    loader = DataLoader(MatchDataset('dataset/test_data.csv'), 1)
    print("Dataset Loaded")
    device = torch.device('cuda:0')

    model = LOLResultModel(190)
    model.load_state_dict(torch.load('checkpoints/model.pth'))
    print("Model created")
    model.to(device)
    model.eval()

    correct_pred = 0
    total = 0
    with torch.no_grad():
        for i, data in enumerate(loader):
            output = model(data['x'].to(device))[0]
            pred = round(output.detach().cpu().numpy()[0])
            real = data['y'].numpy()[0]
            if pred == real:
                correct_pred += 1
            total += 1
    print(f'Predicted {correct_pred} out of {total}: '
          f'{correct_pred * 100 // total}%')
