import sys
import re
import json
import argparse

from typing import List
from tqdm import tqdm


class Entry:
    '''
    Объект класса Entry представляет запись с информацией о пользователе.

    Attributes
    ----------
      email : str
        email пользователя
      weight : str
        вес пользователя
      inn : str
        ИНН пользователя
      passport_series : str
        серия паспорта пользователя
      occupation : str
        профессия пользователя
      age : str
        возраст пользователя
      academic_degree : str
        степень пользователя
      worldview : str
        мировоззрение пользователя
      address : str
        адрес пользователя
    '''
    email: str
    weight: str
    inn: str
    passport_series: str
    occupation: str
    age: str
    academic_degree: str
    worldview: str
    address: str

    def __init__(self, dic: dict):
        self.curdict = dic
        self.email = dic['email']
        self.weight = dic['weight']
        self.inn = dic['inn']
        self.passport_series = dic['passport_series']
        self.occupation = dic['occupation']
        self.age = dic['age']
        self.academic_degree = dic['academic_degree']
        self.worldview = dic['worldview']
        self.address = dic['address']


class Validator:
    '''
    Объект класса Validator представляет валидатор записей.

    Он нужен для проверки введённых пользователем записей о
    email, весе, возрасте, ИНН, серии паспорта, степени, адреса
    на корректность.

    Attributes
    ----------
      entries : List[Entry]
        Список записей
    '''

    entries: List[Entry]

    def __init__(self, entries: List[Entry]):
        self.entries = []

        for i in entries:
            self.entries.append(Entry(i))

        #self.entries = entries

    def parse(self) -> (List[List[str]], List[Entry]):
        '''
        Выполняет проверку корректности записей

        Returns
        -------
          (List[List[str]], List[Entry]):
            Пара: cписок списков неверных записей по названиям ключей
						и список верных записей
        '''

        illegal_entries = []
        legal_entries = []

        for i in self.entries:
            illkeys = self.parse_entry(i)

            if len(illkeys) != 0:
                illegal_entries.append(illkeys)
            else:
                legal_entries.append(i)
        return (illegal_entries, legal_entries)

    def parse_entry(self, entry: Entry) -> List[str]:
        '''
        Выполняет проверку корректности одной записи

        Returns
        -------
          List[str]:
            Список неверных ключей в записи
        '''

        illegal_keys = []

        if not self.check_email(entry.email):
            illegal_keys.append('email')
        elif not self.check_inn(entry.inn):
            illegal_keys.append('inn')
        elif not self.check_passport(entry.passport_series):
            illegal_keys.append('passport_series')
        elif not self.check_weight(entry.weight):
            illegal_keys.append('weight')
        elif not self.check_age(entry.age):
            illegal_keys.append('age')
        elif not self.check_address(entry.address):
            illegal_keys.append('address')
        elif not self.check_occupation(entry.occupation):
            illegal_keys.append('occupation')
        elif not self.check_degree(entry.academic_degree):
            illegal_keys.append('academic_degree')
        elif not self.check_worldview(entry.worldview):
            illegal_keys.append('worldview')

        return illegal_keys

    def check_email(self, email: str) -> bool:
        '''
        Выполняет проверку корректности адреса электронной почты.

        Если в строке присутствуют пробелы, запятые, двойные точки,
        а также неверно указан домен адреса, то будет возвращено False.

        Parameters
        ----------
          email : str
            Строка с проверяемым электронным адресом

        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''
        pattern = "^[^\\s@]+@([^\\s@.,]+\\.)+[^\\s@.,]{2,}$"
        if re.match(pattern, email):
            return True
        return False

    def check_inn(self, inn: str) -> bool:
        '''
        Выполняет проверку корректности ИНН.

        Если строка состоит не из 12-ти цифр, возвращает False

        Parameters
        ----------
          inn : str
            Строка с проверяемым ИНН

        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^\\d{12}$'

        if re.match(pattern, inn):
            return True
        return False

    def check_passport(self, passport: str) -> bool:
        '''
        Выполняет проверку корректности серии паспорта.

        Если строка состоит не из четырёх цифр разделённых попарно пробелом, возвращает False

        Parameters
        ----------
          passport : str
            Строка с проверяемой серией

        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^\\d{2} \\d{2}$'

        if re.match(pattern, passport):
            return True
        return False

    def check_weight(self, weight: str) -> bool:
        '''
        Выполняет проверку корректности веса пользователя.

        Возврашщает True, если вес находится в пределах 25..300

        Parameters
        ----------
          weight : str
            Строка с проверяемым весом

        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        try:
            iweight = int(weight)
        except ValueError:
            return False

        return iweight > 25 and iweight < 300

    def check_age(self, age: str) -> bool:
        '''
        Выполняет проверку корректности возраста пользователя.

        Возврашщает True, если вес находится в пределах 18..100

        Parameters
        ----------
          age : str
            Строка с проверяемым возрастом

        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        try:
            iage = int(age)
        except ValueError:
            return False

        return iage >= 18 and iage < 110

    def check_address(self, address: str) -> bool:
        '''
        Выполняет проверку корректности адреса пользователя.

        Возврашщает True, строка состоит из букв русского/английского алфавита, цифр и знака '-', а также
        строка разделена на улицу и номер дома, состоящего из цифр

        Parameters
        ----------
          address : str
            Строка с проверяемым адресом

        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^[\\wа-яА-Я\\s\\.\\d-]* \\d+$'

        if re.match(pattern, address):
            return True
        return False

    def check_occupation(self, occupation: str) -> bool:
        '''
        Выполняет проверку корректности профессии пользователя.

        Возврашщает True, строка состоит из букв русского/английского алфавита, знака '-' или пробела

        Parameters
        ----------
          occupation : str
            Строка с проверяемой профессией

        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^[a-zA-Zа-яА-Я -]+$'

        if re.match(pattern, occupation):
            return True
        return False

    def check_degree(self, degree: str) -> bool:
        '''
        Выполняет проверку корректности степени пользователя.

        Возврашщает True, строка состоит из букв русского/английского алфавита, знака '-' или пробела

        Parameters
        ----------
          degree : str
            Строка с проверяемой степенью

        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^[a-zA-Zа-яА-Я -]+$'

        if re.match(pattern, degree):
            return True
        return False

    def check_worldview(self, worldview: str) -> bool:
        '''
        Выполняет проверку корректности мировоззрения пользователя.

        Возврашщает True, строка состоит из букв русского/английского алфавита, знака '-' или пробела

        Parameters
        ----------
          worldview : str
            Строка с проверяемым мировоззрением

        Returns
        -------
          bool:
            Булевый результат проверки на корректность
        '''

        pattern = '^[a-zA-Zа-яА-Я -]+$'

        if re.match(pattern, worldview):
            return True
        return False


def show_summary(result: List[List[str]], filename: str = ''):
    '''
      Выдаёт итоговую информацию об ошибках в записях

      Parameters
      ----------
        result : List[List[str]]
          Список списков неверных записей по названиям ключей
    '''

    all_errors_count = 0
    errors_count = {
        "email": 0,
        "weight": 0,
        "inn": 0,
        "passport_series": 0,
        "occupation": 0,
        "age": 0,
        "academic_degree": 0,
        "worldview": 0,
        "address": 0,
    }

    for i in result:
        for j in i:
            errors_count[j] += 1
            all_errors_count += 1

    if filename == '':
        print('\nВсего ошибок: %d\n' % all_errors_count)
        print('Количество ошибок по типам: ')

        for key, value in errors_count.items():
            print(key, ': ', value, sep='')
    else:
        with open(filename, 'w') as file:
            file.write('Всего ошибок: %d\n' % all_errors_count)

            for key, value in errors_count.items():
                file.write(key + ': ' + str(value) + '\n')

def save_in_json(data: List[Entry], filename: str):
  '''
      Выдаёт итоговую информацию о верных записях в формате json

      Parameters
      ----------
        data : List[Entry]
          Список верных записей
        filename : str
          Имя файла для записи
  '''
  f = open(filename, 'w')

  f.write('[')

  for i in data:
    f.write('''
    {
      "email": "%s",
      "weight": %d,
      "inn": "%s",
      "passport_series": "%s",
      "occupation": "%s",
      "age": %d,
      "academic_degree": "%s",
      "worldview": "%s",
      "address": "%s",
    },''' % (i.email,
    i.weight,
    i.inn,
    i.passport_series,
    i.occupation,
    i.age,
    i.academic_degree,
    i.worldview,
    i.address))
  f.write('\n]')
  f.close()


if len(sys.argv) < 2:
  input_file = '21.txt'
  output_file = '21_result.txt'
else:
  parser = argparse.ArgumentParser(
      description='Make users\' entries validation.')
  parser.add_argument('-input_file', metavar='input_file', nargs=1, type=str,
                      help='input file name')
  parser.add_argument('-output_file', metavar='output_file', nargs=1, type=str,
                      help='output file name')

  args = parser.parse_args()

  input_file = args.input_file[0]
  output_file = args.output_file[0]


val = Validator([])

with tqdm(total=100) as progressbar:
    data = json.load(open(input_file, encoding='windows-1251'))
    progressbar.update(60)

    val = Validator(data)
    res = val.parse()

    progressbar.update(40)

    show_summary(res[0], output_file)
    save_in_json(res[1], 'valid_data.txt')

