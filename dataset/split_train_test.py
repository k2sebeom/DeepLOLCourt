import sys
import random


if __name__ == '__main__':
    dataroot = sys.argv[1]
    with open(dataroot, 'r', encoding='utf8') as f:
        raw_data = f.read().split('\n')[:-1]

    header = raw_data.pop(0)
    random.shuffle(raw_data)
    split_idx = int(len(raw_data) * 0.8)
    with open('train_data.csv', 'w') as f:
        f.write(header + '\n')
        for line in raw_data[:split_idx]:
            f.write(line + '\n')
    with open('test_data.csv', 'w') as f:
        f.write(header + '\n')
        for line in raw_data[split_idx:]:
            f.write(line + '\n')
