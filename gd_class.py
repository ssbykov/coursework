# import logging
from googleapiclient.discovery import build
from io import BytesIO
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseUpload
import requests
import json
from pathlib import Path
from progress.bar import IncrementalBar

class GoogleDrive:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    def __init__(self, token):
        self.token = token
        self.flow = InstalledAppFlow.from_client_secrets_file(self.token, self.SCOPES)
        self.creds = self.flow.run_local_server(port=0)
        self.service = build('drive', 'v3', credentials=self.creds)
# метод для создания папки на гугл диске
    def _create_folder(self, folder_name):
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        results = self.service.files().list(q = "mimeType = 'application/vnd.google-apps.folder'",
            spaces='drive',
            fields='nextPageToken, files(id, name)').execute()
        results = list(filter(lambda item: item['name'] == folder_name, results['files']))
        if results:
            return results[0]['id']             
        folder = self.service.files().create(body=folder_metadata).execute()
        return folder.get('id')
# метод для выгрузки фотографий на диск
    def copy_photos_to_disk(self, file_urls_dict, album_name):
        folder_id = self._create_folder(album_name)
        if not len(file_urls_dict):
            print('Нет фотографий для загрузки')
            return
        bar = IncrementalBar('Загрузка файлов:', max = len(file_urls_dict.items()))
        load_files = []
        for key, value in file_urls_dict.items():
            response = requests.get(value[0])
            file_content = BytesIO(response.content) 
            file_metadata = {'name': key + '.jpg', 'parents': [folder_id]}
            media = MediaIoBaseUpload(file_content, mimetype='image/jpeg', resumable=True)
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            if file.get('id'):
                bar.next()
                load_files.append({'file_name': key + '.jpg', 'size': value[1]})
        print(f'\nВсего в директорию "{album_name}" загружено фотографий - {len(load_files)}.')
        file_path = str(Path(__file__).parent.absolute()) + '/load_files.json'
        with open(file_path, 'w') as f:
            json.dump(load_files, f)