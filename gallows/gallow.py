from random import randint
import sqlite3
from time import sleep

class Gallow():
    def __init__(self, words, gallow):
        self.gallow = gallow
        self.words = words
        self.word = self.words[randint(0, len(self.words) - 1)].lower()
        self.res = ('_ ' * len(self.word)).split(' ')
        self.res = self.res[:-1]
        self.yes = True
        self.used = []
        self.count = -1
        self.new = []
        self.win = ''
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
        
    def game(self, word, win, count, yes):
        while yes:
            connection = sqlite3.connect('results.db')
            cursor = connection.cursor()
            nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            letter = input('Введите букву: ').lower()
            if letter in self.used:
                print(' ')
                print('Вы уже вводили эту букву!')
                continue
            elif letter in nums or len(letter) != 1 or letter == ' ':
                print(' ')
                print('Вы ввели не букву!')
                continue
            self.used.append(letter)
            is_there = False
            for i in range(len(word)):
                if letter == word[i]:
                    self.res[i] = letter
                    is_there = True
            if is_there:
                print(''.join(self.res))
            else:
                print('Такой буквы нет!')
                count += 1
                self.new.append(self.gallow[count])
                for i in range(len(self.new)):
                    print(self.new[i])
            if ''.join(self.res) == word:
                print(' ')
                print('Вы победили!')
                yes = False
                win = 'Отгадал(а)'
            elif self.new == self.gallow:
                print(' ')
                print('Вы проиграли!')
                yes = False
                win = 'Не отгадал(а)'
        cursor.execute('INSERT INTO game_results (result, word) VALUES (?, ?)', (win, word))
        connection.commit()
        connection.close()
        print(word)
        sleep(3)
            
    def check_data(self):
        connection = sqlite3.connect('results.db')
        cursor = connection.cursor()

        cursor.execute('SELECT COUNT(*) FROM game_results')
        result_count = cursor.fetchone()[0]

        connection.close()

        if result_count > 0:
            return 'true'
        else:
            return 'false'

    def get_results(self):
        connection = sqlite3.connect('results.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM game_results')
        results = cursor.fetchall()

        for row in results:
            if self.check_data() == 'false':
                print('История пуста!')
                break
            elif self.check_data() == 'true':
                print(f'ID: {row[0]}, Результат: {row[1]}, Слово: {row[2]}')

        connection.close()
        
    def clear_table(self):
        connection = sqlite3.connect('results.db')
        cursor = connection.cursor()

        cursor.execute('DELETE FROM game_results')

        connection.commit()
        connection.close()
        
    def reset_game(self):
        self.word = self.words[randint(0, len(self.words) - 1)].lower()
        self.res = ('_ ' * len(self.word)).split(' ')
        self.res = self.res[:-1]
        self.yes = True
        self.used = []
        self.count = -1
        self.new = []
        self.win = ''
        
    def menu(self):
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
        
    def start_game(self):
        while True:
            new_game = self.menu()
            if new_game == 'start':
                print('                                              ')
                print('----------------------------------------------')
                print('                Игра началась!                ')
                print('----------------------------------------------')
                print('                                              ')
                self.reset_game()
                self.game(self.word, self.win, self.count, self.yes)
            elif new_game == 'history':
                self.get_results()
                sleep(2)
            elif new_game == 'clear':
                self.clear_table()
                print('История успешно было очищена')
                sleep(2)
            elif new_game == 'exit':
                break
            elif new_game == 'error':
                print('Попробуйте еще раз!')    

words = [
    'указатель', 'радуга', 'мармелад', 'Поиск', 'Прятки', 'Сторож', 'Копейка', 'Леопард',
    'Аттракцион', 'Дрессировка', 'Ошейник', 'Карамель', 'Водолаз', 'Защита', 'Батарея',
    'Решётка', 'Квартира', 'Дельфинарий', 'Непогода', 'Вход', 'Полиция', 'Перекрёсток',
    'Башня', 'Стрелка', 'Градусник', 'Бутылка', 'Щипцы', 'Наволочка', 'Павлин', 'Журнал',
    'Карточка', 'Записка', 'Лестница', 'Переулок', 'Сенокос', 'Рассол', 'Закат', 'Сигнализация',
    'Заставка', 'Тиранозавр', 'Микрофон', 'Прохожий', 'Квитанция', 'Пауза', 'Новости',
    'Скарабей', 'Серебро', 'Творог', 'Осадок', 'Песня', 'Корзина', 'Сдача', 'Овчарка', 'Хлопья',
    'Телескоп', 'Микроб', 'Угощение', 'Экскаватор', 'Письмо', 'Пришелец', 'Айсберг',
    'Пластик', 'Доставка', 'Полка', 'Билет', 'Вторник', 'Льдина', 'Интерес', 'Троллейбус',
    'Футболист', 'Лисёнок', 'Пример', 'Баклажан', 'Лягушка', 'Джокер', 'Котлета',
    'Накидка', 'Дикобраз', 'Барбарис', 'Работник', 'Кристалл', 'Доспехи', 'Халва',
    'Велосипед', 'Крючок', 'Кочка', 'Черепаха', 'Петля', 'Осень', 'Яйцо',
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

if __name__ == '__main__':
    game = Gallow(words, gallow)
    game.start_game()