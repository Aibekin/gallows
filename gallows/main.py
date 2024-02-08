from random import randint
import sqlite3
from time import sleep

connection = sqlite3.connect('results.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        result TEXT,
        word TEXT
    )
''')

connection.commit()
connection.close()

words = [
    'человек', 'виселица', 'карнавал', 'дельфинарий',
    'красноречие', 'доцент', 'живодерство', 'перекрёсток',
    'хроника', 'подлокотник', 'скворечник', 'сигнализация',
    'комбинация', 'магнитофон', 'леденец', 'телескоп'
]

gallow = [
    '_______     ',
    '|      |    ',
    '|      |    ',
    '|      0    ',
    '|     /|\   ',
    '|     / \   ',
    '|           ',
    '------------'
]

def filler(word):
    res = ('_ ' * len(word)).split(' ')
    res = res[:-1]
    yes = True
    used = []
    count = -1
    new = []
    win = ''
    while yes:
        connection = sqlite3.connect('results.db')
        cursor = connection.cursor()
        letter = input('Введите букву: ')
        if letter in used:
            print('Вы уже вводили эту букву!')
            continue
        is_there = False
        for i in range(len(word)):
            if letter == word[i]:
                res[i] = letter
                used.append(letter)
                is_there = True
        if is_there:
            print(''.join(res))
        else:
            print('Такой буквы нет!')
            count += 1
            new.append(gallow[count])
            for i in range(len(new)):
                print(new[i])
        if ''.join(res) == word:
            print('Вы победили!')
            yes = False
            win = 'Отгадал(а)'
        elif new == gallow:
            print('Вы проиграли!')
            yes = False
            win = 'Не отгадал(а)'
    cursor.execute('INSERT INTO game_results (result, word) VALUES (?, ?)', (win, word))
    connection.commit()
    connection.close()
    print(word)
    
def check_data():
    connection = sqlite3.connect('results.db')
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM game_results')
    result_count = cursor.fetchone()[0]

    connection.close()

    if result_count > 0:
        return 'true'
    else:
        return 'false'

def get_results():
    connection = sqlite3.connect('results.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM game_results')
    results = cursor.fetchall()

    for row in results:
        if check_data() == 'false':
            print('История пуста!')
            break
        elif check_data() == 'true':
            print(f'ID: {row[0]}, Результат: {row[1]}, Слово: {row[2]}')

    connection.close()
    
def clear_table():
    connection = sqlite3.connect('results.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM game_results')

    connection.commit()
    connection.close()
 
def menu():
    print('                                              ')
    print('----------------------------------------------')
    print('       Добро пожаловать в игру Виселица       ')
    print('----------------------------------------------')
    print('      Чтобы начать игру введите - начать      ')
    print('Чтобы посмотреть историю игр введите - история')
    print('           Чтобы выйти введите выход          ')
    print('----------------------------------------------')
    print('                                              ')
    start = input('Введите что нибудь: ')
    print('                                              ')
    if start.lower() == 'начать':
        return 'start'
    elif start.lower() == 'история':
        return 'history'
    elif start.lower() == 'clear':
        return 'clear'
    elif start.lower() == 'выход':
        return 'exit'
    else:
        return 'error'
    
def start_game():
    while True:
        new_game = menu()
        if new_game == 'start':
            print('                                              ')
            print('----------------------------------------------')
            print('                Игра началась!                ')
            print('----------------------------------------------')
            print('                                              ')
            word = words[randint(0, len(words) - 1)]
            filler(word)
        elif new_game == 'history':
            get_results()
            sleep(2)
        elif new_game == 'clear':
            clear_table()
            print('История успешно было очищена')
            sleep(2)
        elif new_game == 'exit':
            break
        elif new_game == 'error':
            print('Попробуйте еще раз!')
            
if __name__ == '__main__':
    start_game()