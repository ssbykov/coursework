import sys
import logging
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
            sn_client = VKnet('токен ВКонтакте', '5.131')
            network_name = 'VK'
        elif network_id == '2':
            sn_client = OKnet('токен Одноклассники', 'application_key Одноклассники', 'session_secret_key Одноклассники')
            network_name = 'OK'
        elif network_id == '3':
            sn_client = InstaNet('токен Инстаграмм')
            network_name = 'INST'
    logger.info(f'Пользователем выбрана социальная сеть {network_name}.')    
    return sn_client, network_name
# функция для ввода и проверки начальных данных
def input_check(network_name):
    logger.info('Выполнен вход в процедуру input_check().')    
    id_user = ''
    album_id = ''
    user_name = ''
    if network_name != 'INST':
        while not user_name:
            id_user = input('Введите ID пользователя ("0" - свой ID, "q" - выход): ')
            if id_user == 'q':
                logger.info('Выполнен выход из программы на этапе ввода ID пользоваталя.')    
                sys.exit()
            logger.info(f'Введен ID пользоваталя {id_user}.')    
            user_name,id_user = sl_client._get_profile(id_user)
            if not user_name: 
                print('Пользователя с данным ID не существует!')
    else:
        user_name,id_user = sl_client._get_profile('me')
    logger.info(f'Получено имя пользователя {user_name}.')    
    dict_albims = sl_client.get_albums(id_user, user_name)
    logger.info(f'Получен словарь альбомов длинной {len(dict_albims)}.')    
    while album_id not in dict_albims:
        album_id = input('Введите ID альбома из списка ("q" - выход): ')
        logger.info(f'Введен ID альбома {album_id}.')    
        if album_id == 'q':
            logger.info('Выполнен выход из программы на этапе ввода ID альбома.')    
            sys.exit()
    number_photo = ''
    while not number_photo.isdigit():
        number_photo = input('Введите количество фотографий для сохранения (по умолчанию 5): ')
        logger.info(f'Введено количество фотографий "{number_photo}".')    
        if not number_photo:
            number_photo = '5'
            logger.info(f'Количество фотографий по умолчанию "{number_photo}".')    
    dict_input = {
        'sn': sl_client,
        'id_user': id_user,
        'user_name': user_name,
        'album_id': album_id,
        'album_name': dict_albims[album_id],
        'number_photo': number_photo
        }
    logger.info(f'Получен словарь параметров "{dict_input}".')    
    return dict_input
#функция выгрузки файлов на облачный диск
def upload_to_cloud_disk(disk_id):
    logger.info('Выполнен вход в процедуру upload_to_cloud_disk().')    
    while disk_id not in ('q', '1', '2'):
        disk_id =input('Введите номер социальной сети (1-Яндекс диск, 2 - Гугл диск, q-выход): ')
        if disk_id == '2':
            logger.info('Выбран GoogleDrive.')    
            g_disk = GoogleDrive('client_secrets.json')
            g_disk.copy_photos_to_disk(dict_input['sn'].get_album_photo(dict_input['id_user'], dict_input['album_id'], \
                dict_input['number_photo']), dict_input['album_name'])
        elif disk_id == '1':
            logger.info('Выбран YaDisk.')    
            ya_disk = YaDisk('Введите токен')
            ya_disk.copy_photos_to_disk(dict_input['sn'].get_album_photo(dict_input['id_user'], dict_input['album_id'], \
                dict_input['number_photo']), dict_input['album_name'])
        if disk_id == 'q':
            logger.info('Выполнен выход из программы на этапе выбора облачного диска.')    
            sys.exit()

if __name__ == '__main__':
    logging.basicConfig(filename='coursework.log', level=logging.INFO, encoding = 'UTF-8', filemode='w',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('main')
    logger.info("Программа запущена.")    
    sl_client, network_name = select_social_net()
    dict_input = {}
    dict_input = input_check(network_name)
    disk_id = ''
    upload_to_cloud_disk(disk_id)