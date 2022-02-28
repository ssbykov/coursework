import sys
from vk_class import VKnet
from ok_class import OKnet
from insta_class import InstaNet
from ya_disk_class import YaDisk
from gd_class import GoogleDrive

def select_social_net():
    network_id = ''
    while network_id not in ('q', '1', '2', '3'):
        network_id =input('Введите номер социальной сети (1-ВКонтате, 2 - ОК, 3 - Инстаграм, q-выход): ')
        if network_id == 'q':
            sys.exit()
        elif network_id == '1':
            sn_client = VKnet('токен ВКонтакте', '5.131')
            network_name = 'VK'
        elif network_id == '2':
            sn_client = OKnet('токен Одноклассники', 'application_key Одноклассники', 'session_secret_key Одноклассники')
            network_name = 'OK'
        elif network_id == '3':
            sn_client = InstaNet('токен Инстаграмм')
            network_name = 'INST'
    return sn_client, network_name
# функция для ввода и проверки начальных данных
def input_check(network_name):
    id_user = ''
    album_id = ''
    if network_name != 'INST':
        while not id_user.isdigit():
            id_user = input('Введите ID пользователя в цифровом формате ("0" - свой ID, "q" - выход): ')
            if id_user == 'q':
                sys.exit()
        user_name,id_user = sl_client._get_profile(id_user)
    else:
        user_name,id_user = sl_client._get_profile('me')
    if user_name: 
        dict_albims = sl_client.get_albums(id_user, user_name)
    else:
        print('Пользователя с данным ID не существует!')
        sys.exit()
    while album_id not in dict_albims:
        album_id = input('Введите ID альбома из списка ("q" - выход): ')
        if album_id == 'q':
            sys.exit()
    number_photo = ''
    while not number_photo.isdigit():
        number_photo = input('Введите количество фотографий для сохранения (по умолчанию 5): ')
        if not number_photo:
            number_photo = '5'
    dict_input = {
        'sn': sl_client,
        'id_user': id_user,
        'user_name': user_name,
        'album_id': album_id,
        'album_name': dict_albims[album_id],
        'number_photo': number_photo
        }
    return dict_input
#функция выгрузки файлов на облачный диск
def upload_to_cloud_disk(disk_id):
    while disk_id not in ('q', '1', '2'):
        disk_id =input('Введите номер социальной сети (1-Яндекс диск, 2 - Гугл диск, q-выход): ')
        if disk_id == '2':
            g_disk = GoogleDrive('client_secrets.json')
            g_disk.copy_photos_to_disk(dict_input['sn'].get_album_photo(dict_input['id_user'], dict_input['album_id'], \
                dict_input['number_photo']), dict_input['album_name'])
        elif disk_id == '1':
            ya_disk = YaDisk('Токен Яндекс диск')
            ya_disk.copy_photos_to_disk(dict_input['sn'].get_album_photo(dict_input['id_user'], dict_input['album_id'], \
                dict_input['number_photo']), dict_input['album_name'])
        if disk_id == 'q':
            sys.exit()

if __name__ == '__main__':
    sl_client, network_name = select_social_net()
    dict_input = {}
    dict_input = input_check(network_name)
    disk_id = ''
    upload_to_cloud_disk(disk_id)