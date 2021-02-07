

if __name__ == '__main__':
    with open('match_data.csv', 'r', encoding='utf8') as f:
        matches = f.read().split('\n')
    with open('clean_data.csv', 'w', encoding='utf8') as f:
        for m in matches:
            if 'N/A' not in m:
                ms = m.split(',')
                if len(ms) > 5:
                    ms.pop(6)
                    ms.pop(24)
                    ms.pop(42)
                    ms.pop(60)
                    ms.pop(78)
                    ms.pop(102)
                    ms.pop(120)
                    ms.pop(138)
                    ms.pop(156)
                    ms.pop(174)
                f.write(','.join(ms) + '\n')
