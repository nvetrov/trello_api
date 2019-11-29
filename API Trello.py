"""D1.11 Домашнее задание """

# TODO:Обработайте совпадающие имена задач *
# import pdb
import sys

import requests

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.
with open("API_token.txt", "r") as token_f:
    token_key = token_f.readline().strip()

with open("key.txt", "r") as key_f:
    api_key = key_f.readline().strip()

with open("key.txt", "r") as key_f:
    board_id = key_f.readline().strip()

token_key = str(input("token_key:"))
api_key = str(input("api_key:"))
board_id = str(input("board_id:"))

auth_params = {
    'key': str(api_key),
    'token': str(token_key),
}

base_url = "https://api.trello.com/1/{}"


# TODO: Добавьте рядом с названием колонки цифру, отражающую количество задач в ней.
def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # pdb.set_trace()
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'] + " - " + str((len(task_data))))
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'], task['pos'])


def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column_tasks)
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

            # Теперь, когда у нас есть id задачи, которую мы хотим переместить,
    # Получим ID колонки, в которую мы будем перемещать задачу
    column_id = column_check(column_name)
    if column_id is None:
        column_id = add(column_name)['id']
        # И совершим перемещение:
    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column_id, **auth_params})


# TODO: Реализуйте создание колонок.
def add(column_name):
    # pdb.set_trace()
    return requests.post(base_url.format('boards') + '/' + board_id + '/lists',
                         # res = requests.post(base_url.format('lists'),
                         data={'name': column_name, 'idBoard': board_id, **auth_params}).json()


def column_check(column_name):
    column_id = None
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            column_id = column['id']
            return column_id
    return column_id


def create(name, column_name):
    column_id = column_check(column_name)
    if column_id is None:
        column_id = add(column_name)['id']

    # pdb.set_trace()
    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})


if __name__ == "__main__":
    move("New Value", "Готово")
    # if len(sys.argv) <= 2:
    #     read()
    # elif sys.argv[1] == 'create':
    #     create(sys.argv[2], sys.argv[3])
    # # elif sys.argv[1] == 'add':
    # #     add(sys.argv[2])
    # elif sys.argv[1] == 'move':
    #     move(sys.argv[2], sys.argv[3])
    # else:
    #     print('Введите корректные данные')

# python API\ Trello.py create "create" "Готово"
# python API\ Trello.py move "create" "В процессе"
