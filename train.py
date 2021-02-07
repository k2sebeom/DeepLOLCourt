import torch.optim as optim
from torch import nn
from data.match_dataset import MatchDataset
from torch.utils.data import DataLoader
from models.lol_result_model import LOLResultModel
import torch


if __name__ == '__main__':

    EPOCH = 50
    BATCH_SIZE = 32

    loader = DataLoader(MatchDataset('dataset/train_data.csv'), BATCH_SIZE)
    print("Dataset Loaded")
    loss_criterion = nn.BCELoss()
    device = torch.device('cuda:0')

    model = LOLResultModel(190)
    print("Model created")
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    model.to(device)
    for epoch in range(EPOCH):
        loss_data = 0
        for i, data in enumerate(loader):
            output = model(data['x'].to(device))
            loss = loss_criterion(output, data['y'].unsqueeze(1).float().to(device))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss_data = loss.data
        print(f'Epoch {epoch}: {loss_data}')
    torch.save(model.state_dict(), 'checkpoints/model.pth')
