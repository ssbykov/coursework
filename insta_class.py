import requests
from datetime import datetime as dt
import sys

class InstaNet:
    URL = 'https://graph.instagram.com/'
    def __init__(self, token: str):
        self.params = {'access_token': token}
# метод для получения данных пользователя по ID
    def _get_profile(self, owner_id):
        _get_profile_params = {'fields': 'id,username'}
        response = requests.get(self.URL + owner_id, params={**self.params, **_get_profile_params})
        self._error(response, self._get_profile.__name__)
        response = response.json()
        return [response['username'], response['id']]
# метод для получения данных по альбомам пользователя по ID пользователя и вывод на консоль
    def get_albums(self, owner_id, user_name):
        dict_albims = {}
        get_albums_params = {'fields': 'id,media_url,caption,timestamp,media_type,permalink,username'}
        response = requests.get(self.URL + owner_id +'/media', params={**self.params, **get_albums_params})
        self._error(response, self.get_albums.__name__)
        response = response.json()
        print(f"У пользоателя {user_name} всего альбомов: {len(response['data'])}.")
        for album in response['data']: 
            print(f"id: '{album['id']}', название '{album['caption']}'")
            dict_albims[str(album['id'])] = album['caption']
        return dict_albims
# метод для получения данных по фотографиям по ID пользоателя и ID альбома для загрузки
    def get_album_photo(self, owner_id, album_id, number_photo):
        dict_res = {}
        get_album_photo_params = {'fields': 'media_type,media_url'}
        response = requests.get(self.URL + album_id + '/children', params={**self.params, **get_album_photo_params})
        self._error(response, self.get_album_photo.__name__)
        response = response.json()
        if int(number_photo) > len(response['data']):
            number_photo = len(response['data'])
        for item in range(int(number_photo)):
            if response['data'][item]['media_type'] == 'IMAGE':
                dict_res[response['data'][item]['id']] = [response['data'][item]['media_url'], response['data'][item]['media_type']]
        return dict_res
#метод для вывода сообщений об ошибке
    def _error(self, response, method_name):
        if str(response) != '<Response [200]>' and not 'error' in response.json():
            print(f'{response} - запрос не прошел. Возможно вы ввели недействующий токен.')
            sys.exit()
        method_name_dict = {'_get_profile': 'по пользователю', 'get_albums': 'по альбомам', 'get_album_photo': 'по фотографиям'}
        if 'error' in response.json():
            print(f"При запросе данных {method_name_dict[method_name]} возникла ошибка: {response.json()['error']['code']}"
            f" - {response.json()['error']['message']}.")
            sys.exit()
