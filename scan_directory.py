# Получение адрессов файлов игры относительно корневой папки

import os

bundle_dir_path = os.path.dirname(__file__) # Сдесь у нас показан путь до месторасположения скрипта, тоесть до нашей папки

def get_relative_files_path(bundle_dir_path):
    list_of_path = [] # список с относительными путями до файлов в корневой папке
    for adress, dirs, files in os.walk(bundle_dir_path):
        for file in files:
            full_address = os.path.join(adress, file) # полный адрес до файла
            relative_files_path = './' + os.path.relpath(full_address, bundle_dir_path) # получаем относительный адрес до файла
            list_of_path.append(relative_files_path.replace('\\', '/')) # добавляем относительный адрес в список + меняем символ "\" на "/" что бы linux  нормально открыл
    return list_of_path

list_of_path = get_relative_files_path(bundle_dir_path) # список с относительным путем до файла (относительно корневой папки)