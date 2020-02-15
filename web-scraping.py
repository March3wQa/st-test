import requests as rq
import json
from bs4 import BeautifulSoup

url = 'https://shinden.pl/genre/'
index = 0
data = {
    'codes': {},
    'content': {
        'genre': [],
        'target_group': [],
        'entity': [],
        'setting': [],
        'tag': [],
        'studio': [],
        'type': [],
        'publisher': [],
        'precursor': []
    }
}

while index < 25:
    response = rq.get(url+str(index))
    try:
        data['codes'][response.status_code] += 1
    except KeyError:
        data['codes'][response.status_code] = 1
    print(
        f'{index}\t=> [{response.status_code} - {response.reason}]')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features='html.parser')
        info_type = soup.find(
            'h1', attrs={'class': ['box-title', 'h2']}).contents[3].contents[0].lower()
        info_value = soup.find(
            'h1', attrs={'class': ['box-title', 'h2']}).contents[6].replace('\n', '')
        if info_type == 'studio':
            data['content']['studio'].append((index, info_value))
        elif info_type == 'gatunki':
            data['content']['genre'].append((index, info_value))
        elif info_type == 'miejsce i czas':
            data['content']['setting'].append((index, info_value))
        elif info_type == 'grupy docelowe':
            data['content']['target_group'].append((index, info_value))
        elif info_type == 'rodzaje postaci':
            data['content']['entity'].append((index, info_value))
        elif info_type == 'pozostałe tagi':
            data['content']['tag'].append((index, info_value))
        elif info_type == 'typy produkcji':
            data['content']['type'].append((index, info_value))
        elif info_type == 'wydawnictwa':
            data['content']['publisher'].append((index, info_value))
        elif info_type == 'pierwowzór':
            data['content']['precursor'].append((index, info_value))
        else:
            print(f'{index}\t => unknown type: {info_type}')
    index += 1

with open('data.json', 'w') as out_file:
    out_file.write(json.dumps(data, indent=2))
