import random
import csv
from pathlib import Path


# Функция для чтения нецензурных слов из файла
def read_cens_word():
    data_path = Path.cwd()/ "dataset" / "cens_word.csv"
    cens_word_list = []
    with open(data_path,mode='r') as r_file:
        file_reader = csv.reader(r_file,delimiter=';',lineterminator="\r")
        for cens_word in file_reader:
            cens_word_list.append(cens_word[0])

    return cens_word_list

# Функция для чтения обычных слов из файла
def read_norm_word():
    data_path = Path.cwd() / "dataset" / "all_word.csv"
    word_list = []
    with open(data_path, mode="r") as r_file:
        file_reader = csv.reader(r_file, delimiter=";", lineterminator="\r")
        for word in file_reader:
            word_list.append(word[0])
    return word_list

# Списки необходимых слов
cens_word_list = read_cens_word()
word_list = read_norm_word()

# Функция для удаления ненужных пробелов
def spacedel(sentencet):
    lisw = sentencet.split(" ")
    # переменная для слов, разделённых пробелами (с л о в о)
    finword = ""
    n = -1
    for ind,i in enumerate(lisw):
        # Проверка одиночных символов
        if len(i) == 1 and i != " ":
            if n == -1:
                n = ind
            # Формирование слова
            finword += i

            # Заглушка одиночно стоящих букв разделённого слова
            if ind != n:
                lisw[ind] = "!цЩВкм"

        # Проверка на завершение разделённого слова
        elif len(i)>1 and finword != "":
            # Применение сформированного слова
            lisw[n] = finword
            n = -1
            finword = ""

    # Условие для крайнего слова в предложении
    if finword != "":
        lisw[n] = finword

    # Формирование обработанного изображения
    final_text = " ".join(lisw)

    # Удаление заглушек
    final_text = final_text.replace("!цЩВкм", "")

    return final_text

# Функция разбиения текста на n-граммы
def n_gramm(mess,n_gramm=3):
    # Предобработка
    mess = spacedel(mess)
    messlist = mess.split(" ")

    # Список для n-грамм
    finallist = []
    # Обход слов
    for i in messlist:
        # Условие разделения на n-граммы
        if len(i) > n_gramm:
            # Индексы разделения
            endlet = n_gramm
            startlet = 0
            # Цикл разделения
            while endlet < len(i) + 1:
                finallist.append(i[startlet:endlet])
                endlet += 1
                startlet += 1
        # Условие для слов с длиной меньше n_gramm
        elif i != "" and len(i) <= n_gramm:
            finallist.append(i)
    # формирование текста из n-грамм
    ngrammlist = " ".join(finallist)
    return ngrammlist

# Функция для сохранения данных
def save_data(fin_list,file_name="word_dataset"):
    data_path = Path.cwd() / "dataset" / f"{file_name}.csv"
    with open(data_path, mode="w") as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        for i in range(len(fin_list)):
            file_writer.writerow([fin_list[i][0],fin_list[i][1]])

# Функция для создания датасета
def create_dataset(data_volume,n_gramm=False):
    # Список для нецензурной лексики
    cens_list = []
    # Список сгенерированных данных
    fin_list = []
    # Цикл для создания предложений
    for b in range(data_volume):
        data = []
        # Копируем словарь матов
        if len(cens_list) == 0:
            cens_list = cens_word_list.copy()

        # Определяем кол-во слов и наличие мата
        volume_word = random.randint(1,100)
        cens_numb = -1
        # Указатель наличия нецензурных слов в предложении
        availability_cens = random.randint(0,1)

        sentence = ""
        # Генерация индекса слова в предложении
        if availability_cens == 1:
            cens_numb = random.randint(0,volume_word-1)
        # Цикл генерации предложения
        for i in range(volume_word):
            # Условие добавление нецензурного слова
            if i == cens_numb:
                mat = cens_list[random.randint(0,len(cens_list)-1)]
                sentence += mat + " "
                # Удаление использованного слова
                cens_list.remove(mat)
            # Условие использования нормального слова
            else:
                word = random.randint(0, len(word_list)-1)
                sentence += word_list[word] + " "

        # Добавление метки предложения
        data.append(availability_cens)
        # Объединение разделённых слов
        sentence = spacedel(sentence)
        # Условие разбиения текста на n-граммы
        if n_gramm:
            sentence = n_gramm(sentence)
        # Добавление сгенерированного предложения
        data.append(sentence)
        fin_list.append(data)

    save_data(fin_list)

    return 1

create_dataset(15)

