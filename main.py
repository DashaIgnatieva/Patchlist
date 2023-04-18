# Главная часть программы. Отсюда запускаются все остальные скрипты

import os
import hashlib # библиотека по работе с хешами

bundle_dir_path = os.path.dirname(__file__) # Здесь у нас показан путь до месторасположения скрипта, то есть до нашей папки

def get_relative_files_path(bundle_dir_path): # функция для получения относительного пути до файла
    list_of_path = [] # список с относительными путями до файлов в корневой папке
    for adress, dirs, files in os.walk(bundle_dir_path):
        for file in files:
            full_address = os.path.join(adress, file) # полный адрес до файла
            relative_files_path = './' + os.path.relpath(full_address, bundle_dir_path) # получаем относительный адрес до файла
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

list_of_path = get_relative_files_path(bundle_dir_path) # список с относительным путем до файла (относительно корневой папки)

dict_with_file_address_and_hash = {} # словарь, в котором будут адресса файлов и их хеши

for file_address in list_of_path: # итерируем список с адрессами
    file_hash = get_file_hash(file_address) # присваиваем текущему элементу хеш
    dict_with_file_address_and_hash[file_address] = file_hash # записываем адрес и хеш его файла в словарь

print(dict_with_file_address_and_hash)