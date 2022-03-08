import logging
import hashlib
import requests
from datetime import datetime as dt
import sys

class OKnet:
    URL = 'https://api.ok.ru/fb.do?'
    def __init__(self, token: str, application_key: str, session_secret_key: str):
        self.params = {
            'format': 'json',
            'application_key': application_key    
        }
        self.token = token
        self.session_secret_key = session_secret_key
        self.logger = logging.getLogger('main.OKnet')
# метод для получения данных пользователя по ID
    def _get_profile(self, owner_id):
        self.logger.info('Выполнен вызов метода _get_profile()')
        if owner_id == '0':
            _get_profile_params = {'fields': 'NAME','method': 'users.getCurrentUser'}
        else:
            _get_profile_params = {'uids': owner_id,'fields': 'NAME','method': 'users.getInfo'}
        response = self._response(self._get_profile.__name__, {**self.params, **_get_profile_params})
        if len(response) == 1:
                return [response[0]['name'],response[0]['uid']]
        elif response:
                return [response['name'],response['uid']]
        else:
            return ['','']
# метод для получения данных по личному альбому "личные фотографии" по ID пользователя и вывод на консоль
    def _get_own_albums(self, owner_id):
        self.logger.info('Выполнен вызов метода _get_own_albums()')
        get_albums_params = {
            'fid': owner_id,
            'detectTotalCount': True,
            'fields': 'ALBUM.AID',
            'method': 'photos.getPhotos',
        }
        response = self._response(self._get_profile.__name__, {**self.params, **get_albums_params})
        return response["totalCount"]
# метод для получения данных по альбомам пользователя по ID пользователя и вывод на консоль
    def get_albums(self, owner_id, user_name):
        self.logger.info('Выполнен вызов метода get_albums()')
        list_albims = []
        list_albims += [{'aid': '0','photos_count': self._get_own_albums(owner_id), 'title': 'Личные фотографии'}]
        hasMore = True
        pagingAnchor = ''
        while hasMore:
            get_albums_params = {
                'fid': owner_id,
                'count': 100,
                'fields': 'ALBUM.AID,ALBUM.PHOTOS_COUNT,ALBUM.title',
                'method': 'photos.getAlbums',
                'pagingAnchor': pagingAnchor
            }
            response = self._response(self._get_profile.__name__, {**self.params, **get_albums_params})
            hasMore = response['hasMore']
            pagingAnchor = response['pagingAnchor']
            list_albims += (x for x in response['albums'] if x['photos_count'] > 0)
        print(f"У пользоателя {user_name} всего альбомов с фотографиями: {len(list_albims)}.")
        for album in list_albims: 
            print(f"id: '{album['aid']}', фотографий {album['photos_count']}, название '{album['title']}'")
        return {x['aid']:x['title'] for x in list_albims}
# метод для получения данных по фотографиям в альбоме
    def get_album_photo(self, owner_id, album_id, number_photo):
        self.logger.info('Выполнен вызов метода get_album_photo()')
        dict_res = {}
        hasMore = True
        pagingAnchor = ''
        number_photo = int(number_photo)
        if album_id == '0':
            album_id = ''
        if number_photo < 100:
            count = number_photo
        else:
            count = 100
        while hasMore and number_photo > 0:
            get_album_photo_params = {
                'fid': owner_id,
                'aid': album_id,
                'count': count,
                'fields': 'PHOTO.ID,PHOTO.PIC_MAX,PHOTO.LIKE_COUNT,PHOTO.CREATED_MS',
                'method': 'photos.getPhotos',
                'anchor': pagingAnchor
            }
            response = self._response(self._get_profile.__name__, {**self.params, **get_album_photo_params})
            hasMore = response['hasMore']
            pagingAnchor = response['anchor']
            number_photo -= 100
            for item in response['photos']:
                file_name = str(item['like_count'])
                file_url = item['pic_max']
                file_time = dt.fromtimestamp(item['created_ms']//1000).strftime('%Y_%m_%d_%H_%M_%S')
                if dict_res.get(f"{file_name}_{file_time}"):
                    dict_res[f"{file_name}_{file_time}_{item['id']}"] = [file_url, 'pic_max'] 
                elif dict_res.get(file_name):
                    dict_res[f"{file_name}_{file_time}"] = [file_url, 'pic_max']
                else:
                    dict_res[file_name] = [file_url, 'pic_max']
        return dict_res
#метод хеширования и отправки запросов за сервер
    def _response(self, method_name, hash_params):
        method_name_dict = {'_get_profile': 'по пользователю', 'get_albums': 'по альбомам', 'get_album_photo': 'по фотографиям'}
        hash_str = ''.join([f'{k}={v}' for k, v in sorted(hash_params.items(),\
            key=lambda hash_params: hash_params[0])]) + self.session_secret_key
        sig = hashlib.md5(bytes(hash_str, encoding='utf-8')).hexdigest()
        try:
            response = requests.get('https://api.ok.ru/fb.do', params={**hash_params, **{'access_token': self.token}, **{'sig': sig}})
        except Exception as exc:
            self.logger.error(exc)
            sys.exit()
        self.logger.info(response)
        response = response.json()
        if 'error_code' in response:
            str_error = f"При запросе данных {method_name_dict[method_name]} возникла ошибка: {response['error_code']}" \
                f" - {response['error_msg']}."
            self.logger.error(str_error)
            print(str_error)
            sys.exit()
        return response