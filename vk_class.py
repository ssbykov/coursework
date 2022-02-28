import requests
from datetime import datetime as dt
import sys

class VKnet:
    URL = 'https://api.vk.com/method/'
    def __init__(self, token: str, version: str):
        self.params = {
            'access_token': token,
            'v': version    
        }
# метод для получения данных пользователя по ID
    def _get_profile(self, id_user):
        _get_profile_params ={}
        if id_user != '0':
            _get_profile_params = {'user_ids': id_user}
        response = requests.get(self.URL + 'users.get', params={**self.params, **_get_profile_params})
        self._error(response, self._get_profile.__name__)
        response = response.json()
        if response['response']:
                return [f"{response['response'][0]['first_name']} {response['response'][0]['last_name']}", str(response['response'][0]['id'])]
        else:
            return ['','']
# метод для получения данных по альбомам пользователя по ID пользователя и вывод на консоль
    def get_albums(self, owner_id, user_name):
        dict_albims = {}
        get_albums_params = {
            'owner_id': owner_id,
            'need_system': 1,
            'photo_sizes': True
        }
        response = requests.get(self.URL + 'photos.getAlbums', params={**self.params, **get_albums_params})
        self._error(response, self.get_albums.__name__)
        response = response.json()
        print(f"У пользоателя {user_name} всего альбомов: {response['response']['count']}.")
        for album in response['response']['items']: 
            print(f"id: '{album['id']}', фотографий {album['size']}, название '{album['title']}'")
            dict_albims[str(album['id'])] = album['title']
        return dict_albims
# метод для получения данных по фотографиям по ID пользоателя и ID альбома для загрузки
    def get_album_photo(self, owner_id, album_id, number_photo):
        size_dict = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
        dict_res = {}
        get_album_photo_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'count': number_photo,
            'extended': 1,
            'photo_sizes': True
        }
        response = requests.get(self.URL + 'photos.get', params={**self.params, **get_album_photo_params})
        self._error(response, self.get_album_photo.__name__)
        response = response.json()
        file_url = []
        for item in response['response']['items']:
            file_name = str(item['likes']['count'])
            file_url = max(item['sizes'], key = lambda x: size_dict[x["type"]])
            file_time = dt.fromtimestamp(item['date']).strftime('%Y_%m_%d_%H_%M_%S')
            if dict_res.get(f"{file_name}_{file_time}"):
                dict_res[f"{file_name}_{file_time}_{item['id']}"] = [file_url['url'], file_url['type']] 
            elif dict_res.get(file_name):
                dict_res[f"{file_name}_{file_time}"] = [file_url['url'], file_url['type']]
            else:
                dict_res[file_name] = [file_url['url'], file_url['type']]
        return dict_res
#метод для вывода сообщений об ошибке
    def _error(self, response, method_name):
        if str(response) != '<Response [200]>':
            print(f'{response} - запрос не прошел.')
            sys.exit()
        method_name_dict = {'_get_profile': 'по пользователю', 'get_albums': 'по альбомам', 'get_album_photo': 'по фотографиям'}
        if 'error' in response.json():
            print(f"При запросе данных {method_name_dict[method_name]} возникла ошибка: {response.json()['error']['error_code']}"
            f" - {response.json()['error']['error_msg']}.")
            sys.exit()
