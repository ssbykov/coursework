import requests
import json
from pathlib import Path
from progress.bar import IncrementalBar

class YaDisk:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
# метод для создания папки на яндекс диске
    def _create_folder(self, folder_path):
        folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        requests.put(folder_url, headers=self.headers, params={'path': folder_path})
# метод для выгрузки фотографий на диск
    def copy_photos_to_disk(self, file_urls_dict, album_name):
        self._create_folder(album_name)
        if not len(file_urls_dict):
            print('Нет фотографий для загрузки')
            return
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        bar = IncrementalBar('Загрузка файлов:', max = len(file_urls_dict.items()))
        load_files = []
        for key, value in file_urls_dict.items():
            params = {'path': f'{album_name}/{key}.jpg', 'url': value[0]}
            response = requests.post(upload_url, headers=self.headers, params=params)
            if response.status_code == 202:
                bar.next()
                load_files.append({'file_name': key + '.jpg', 'size': value[1]})
            else:
                print(f'Код ошибки:{response.status_code}')
        print(f'\nВсего в директорию "{album_name}" загружено фотографий - {len(load_files)}.')
        file_path = str(Path(__file__).parent.absolute()) + '/load_files.json'
        with open(file_path, 'w') as f:
            json.dump(load_files, f)