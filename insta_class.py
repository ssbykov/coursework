import logging
import requests
from datetime import datetime as dt
import sys

class InstaNet:
    URL = 'https://graph.instagram.com/'
    def __init__(self, token: str):
        self.params = {'access_token': token}
        self.logger = logging.getLogger('main.InstaNet')
# метод для получения данных пользователя по ID
    def _get_profile(self, owner_id):
        self.logger.info('Выполнен вызов метода _get_profile()')
        _get_profile_params = {'fields': 'id,username'}
        response = self._response(self._get_profile.__name__, owner_id, {**self.params, **_get_profile_params})
        return [response['username'], response['id']]
# метод для получения данных по альбомам пользователя по ID пользователя и вывод на консоль
    def get_albums(self, owner_id, user_name):
        self.logger.info('Выполнен вызов метода get_albums()')
        dict_albims = {}
        get_albums_params = {'fields': 'id,media_url,caption,timestamp,media_type,permalink,username'}
        response = self._response(self._get_profile.__name__, owner_id  + '/media', {**self.params, **get_albums_params})
        print(f"У пользоателя {user_name} всего альбомов: {len(response['data'])}.")
        for album in response['data']: 
            print(f"id: '{album['id']}', название '{album['caption']}'")
            dict_albims[str(album['id'])] = album['caption']
        return dict_albims
# метод для получения данных по фотографиям по ID пользоателя и ID альбома для загрузки
    def get_album_photo(self, owner_id, album_id, number_photo):
        self.logger.info('Выполнен вызов метода get_album_photo()')
        dict_res = {}
        get_album_photo_params = {'fields': 'media_type,media_url'}
        response = self._response(self._get_profile.__name__, album_id  + '/children', {**self.params, **get_album_photo_params})
        if int(number_photo) > len(response['data']):
            number_photo = len(response['data'])
        for item in range(int(number_photo)):
            if response['data'][item]['media_type'] == 'IMAGE':
                dict_res[response['data'][item]['id']] = [response['data'][item]['media_url'], response['data'][item]['media_type']]
        return dict_res
#метод для вывода сообщений об ошибке
    def _response(self, method_name, response_method_name, response_params):
        try:
            response = requests.get(self.URL + response_method_name, response_params)
        except Exception as exc:
            self.logger.error(exc)
            sys.exit()
        self.logger.info(response)
        if str(response) != '<Response [200]>' and response._content == b"Sorry, this content isn't available right now":
            print(f'{response} - запрос не прошел. {response._content}')
            self.logger.error(response._content)
            sys.exit()
        method_name_dict = {'_get_profile': 'по пользователю', 'get_albums': 'по альбомам', 'get_album_photo': 'по фотографиям'}
        if 'error' in response.json():
            str_error = f"При запросе данных {method_name_dict[method_name]} возникла ошибка: {response.json()['error']['code']}"\
                f" - {response.json()['error']['message']}."
            print(str_error)
            self.logger.error(str_error)
            sys.exit()
        return response.json()
