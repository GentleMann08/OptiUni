# Импорты
import json


# Функция для добавления новых данных в json-файл
def addData(file_path, key, value):
    with open(file_path, 'r', encoding='utf-8-sig') as json_file:
        data = json.load(json_file)

    data[key] = value

    with open(file_path, 'w', encoding='utf-8-sig') as json_file:
        json.dump(data, json_file, indent=8, ensure_ascii=False)

    return 0

# Функция для удаления данных из json
def delData(file_path, key):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    if key in data:
        del data[key]

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=8)

    return 0


# Функция для чтения данных из json
def getData(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as json_file:
        data = json.load(json_file)

    return data

# Функция для проверки наличия ключа в файле json
def isIn(file_path, key):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    if key in data:
      return True
    else:
      return False

