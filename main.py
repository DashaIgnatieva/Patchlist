# Cкрипт для получения для сравнения списка файлов

import sys
import os
import hashlib # библиотека по работе с хешами
import json # модуль для работы с json-ом. Лично я использую его, что бы записать в него словарь с адресами и хешами файлов
import zipfile # модуль для работы с zip файлами

class Patchlist:

    """This class keep the data to be written to the JSON"""
    
    def __init__(self, list_with_paths_and_hashes, version=0):
        self.version = version
        self.files = list_with_paths_and_hashes

def get_relative_files_path(dir_address): # функция для получения относительного пути до файла
    list_of_path = [] # список с относительными путями до файлов в корневой папке
    for adress, dirs, files in os.walk(dir_address):
        for file in files:
            full_address = os.path.join(adress, file) # полный адрес до файла
            relative_files_path = f'./{os.path.relpath(full_address, dir_address)}' # получаем относительный адрес до файла
            list_of_path.append(relative_files_path.replace('\\', '/')) # добавляем относительный адрес в список + меняем символ "\" на "/" что бы linux  нормально открыл
    return list_of_path

def get_file_hash(file_name): # функция для получения хеша файла
    file_hash = hashlib.sha1() # хешируем в нужном нам формате
    
    with open(file_name, 'rb') as file: # открываем файл в двоичном коде
        chunk = 0
        while chunk != b'': # цикл заканчивается тогда, когда в файле не осталось данных
            chunk = file.read(1024) # указываем, сколько читается за раз
            file_hash.update(chunk) 
    return file_hash.hexdigest()

def zipfiles(files_addresses, dir_address):
    '''
    files_addresses - There are addresses' files for a zip archiv
    dir_address - There is a directory's address where the files will be written
    '''
    os.chdir(dir_address) # переходим в папку, в которую будут записаны файлы
    for adress, dirs, files in os.walk(files_addresses):
        for file in files:

            dir_in_path = os.path.dirname(os.path.relpath(os.path.join(adress, file), files_addresses)) # получаем папки в относительном пути до файла
            rel_path = os.path.join(dir_in_path, file) # получаем относительный адрес до файла с папками относительно верхней папки
            if not os.path.isdir(os.path.join(dir_address, dir_in_path)): # проверяем, есть ли по указанному адресу папка
                os.mkdir(os.path.join(dir_address, dir_in_path)) # если папки нет, то создаем ее. 

            new_archive = zipfile.ZipFile(f'./{rel_path}.zip', 'w')
            with new_archive as na: # запись одного файла в архив
                na.write(filename=os.path.join(adress, file), arcname=file,  compress_type=zipfile.ZIP_DEFLATED) # В arcname=filename передаем нужное нам имя файла
            print(f'Фаил "{rel_path}" записан успешно')

try:
    os.path.isdir(sys.argv[1]) # тут мы пытаемся получить корректный адрес до папки с файлами игры для запуска нашего скрипта
except:
    print('Directory not found. Enter a valid address') # если адрес не подходит, выдаем ошибку
    sys.exit()

bundle_dir_path = os.path.dirname(__file__) # Здесь у нас показан путь до месторасположения скрипта, то есть до нашей папки
dir_for_pathlist = sys.argv[1] # сохраняем переданный нам адрес папки для файлов которой надо сделать патч-лист в отдельную переменную

list_of_path = get_relative_files_path(dir_for_pathlist) # список с относительным путем до файла (относительно корневой папки)

dict_with_file_address_and_hash = {} # словарь, в котором будут адресса файлов и их хеши

os.chdir(dir_for_pathlist) # здесь мы открываем папку с файлами, которые мы записали в патч-лист, иначе скрипт будет пытаться найти их рядом с собой

for file_address in list_of_path: # итерируем список с адрессами
    file_hash = get_file_hash(file_address) # присваиваем текущему элементу хеш
    dict_with_file_address_and_hash[file_address] = file_hash # записываем адрес и хеш его файла в словарь

data_for_json = Patchlist(dict_with_file_address_and_hash) # передаем словарь с адресами в класс

with open(os.path.join(bundle_dir_path, 'patchlist.json'), 'w', encoding='utf-8') as data_to_write_to_json: # тут указываем место, куда записываем файл, как назвать документ для записи и его формат.
    data_writing = json.dump(data_for_json.__dict__, data_to_write_to_json, sort_keys=True, indent=4, ensure_ascii=False) # собственно, записываем в JSON

address_for_zip = os.path.join(bundle_dir_path, os.path.basename(os.path.normpath(f'{dir_for_pathlist}_patch')))

os.mkdir(address_for_zip) # создаем папку, в которую запишем заархивированные файлы

zipfiles(dir_for_pathlist, address_for_zip) # архивируем нужные нам файлы и сохраняем рядом с нашим скриптом

print('patchlist.json создан. Пожалуйста, укажите правильную версию patchlist.json вручную')