import pickle
import threading
#import keras
#import tensorflow
from tensorflow import keras
#from tensorflow.keras.preprocessing.text import Tokenizer
import numpy
#from tensorflow.keras.preprocessing.sequence import pad_sequences
import discord
from discord.ext import commands, tasks
from discord.utils import get
import time
import sqlite3
import random
import schedule
from threading import Thread,Event
import re


#   Создаём подключение к БД и таблицу

connect = sqlite3.connect("Discord.sqlite")
cur = connect.cursor()

# Добавить поля для угроз и nsfw картинок,призыв к суициду.
# грубого, насильственного характера, жестокости, призывы к таковым, сообщения экстремистского толка.употребление наркотиков.
cur.execute("""CREATE TABLE IF NOT EXISTS clientservers(
            servername TEXT,
            serverid INT,
            payinfo INT,
            time INT,
            addtime INT,
            onemonth TEXT,
            threemonth TEXT
            threats INT,
            NSFW INT);
            """)
#cur.execute("DROP TABLE clientservers") 923622240304660530
global result
connect.commit()
cur.execute("SELECT * FROM clientservers")
result = cur.fetchall()
print(result)

def spacedel(sent):
    #word = "предложение с вот таким с л о в о м"
    lisw = sent.split(" ")
    #coplist = lisw.copy()
    finword=''
    #print(coplist)
    n = -1
    for ind,i in enumerate(lisw):
        if len(i) == 1 and i != " ":
            if n == -1:
                n = ind
            #print(ind,i)
            finword+=i
            #print(n)
            if ind != n:
                lisw[ind] = "!цЩВкм"
        elif len(i)>1 and finword!="":
            lisw[n] = finword
            #print(lisw)
            n = -1
            finword=""
    #print(finword)
    if finword != "":
        lisw[n] = finword
        finword = ''
    while "!цЩВкм" in lisw:
        lisw.remove("!цЩВкм")
    messageres = " ".join(lisw)
    #print(messageres)
    return messageres
def n_gramm(mess):
    mess = re.sub("[!»()+,-./:;<=>[\\]^`{|}~\t\n«»]", " ", mess)
    mess = spacedel(mess)
    messlist = mess.split(" ")
    finallist = []
    for i in messlist:
        if len(i) > 3:
            endlet = 3
            startlet = 0
            while endlet < len(i) + 1:
                finallist.append(i[startlet:endlet])
                endlet += 1
                startlet += 1
        elif i != "" and len(i) <= 3:
            finallist.append(i)
    ngrammlist = " ".join(finallist)
    return ngrammlist
#   Функция для заполнения данных сервера
def guildup():
    for i in bot.guilds:
        clientserver = (f"{i.name}", f"{i.id}", "-1", "-5","0", keycreate(), keycreate())
        cur.execute("INSERT INTO clientservers VALUES(?,?,?,?,?,?,?)", clientserver)
        connect.commit()

#   Функция для обновления ключей
def updatekey():
    for i in bot.guilds:
        i = i.id
        cur.execute("UPDATE clientservers set onemonth = ?,threemonth = ? WHERE serverid = ?",
                    (keycreate(), keycreate(), i,))
        connect.commit()

#   Функция для создания ключей
def keycreate():
    lists = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
             "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "1",
             "2", "3", "4", "5", "6", "7", "8", "9", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    key = random.choices(lists, k=random.randint(12, 16))
    keystr = ""
    for i in range(len(key)):
        keystr += key[i]
    return keystr

#   Импортируем данные

model = keras.models.load_model("east_model4.h5")
with open('Tokenizer3.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
wordsind = tokenizer.word_index
print(111,wordsind)
def printtoken():
    n = 1
    for i in tokenizer.word_index:
        print("[ ", n, " ] - ", i)
        n += 1

#   Функция для запуска нейронной сети

def matmassage(mess):
    #sent2 =[]
    #mess = re.sub("[’!»#$%&()*+,-./:;<=>?@\\]^_`{|}~\t\n]", "", mess)
    #mess = list(mess.replace(" ", ""))
    #massage = " ".join(mess)
    #print(massage)
    #sent2.append(words)
    #massage = list(mess)
    #massage = " ".join(massage)
    massage = mess
    #print(massage)
    text = massage.split(" ")
    if len(text) >= 1000:
        text = text[0:1000]
        zerotext = []
    else:
        zerotext = [0] * (1000 - len(text))
    # Функция лежит в sound
    sequence = tokenizer.texts_to_sequences([massage])
    #print("1224",type(sequence))
    data = numpy.asarray([zerotext+sequence[0]])
    #print(data)
    #data = pad_sequences(sequence, maxlen=1000)
    #print(data,type(data),len(data))
    result = model.predict(data)
    for b in result:
        print(b, " - ", massage)
        return b

#   Функция для обновления времени работы бота для серверов

def updatetime():
    connect = sqlite3.connect("D:\Discord.sqlite")
    curr = connect.cursor()
    curr.execute("SELECT serverid,payinfo,time,addtime FROM clientservers")
    runresult = curr.fetchall()
    print(2)
    for i in runresult:
        if i[1] == -1 or i[2] <= 0:
            pass
        else:
            curr.execute("UPDATE clientservers set time = ?,addtime = ? WHERE serverid = ?",(i[2] - (24 - i[3]), 0, i[0],))
    connect.commit()
    print(1234)

#   Функция для запуска проверочных сигналов

def runtime():
    while True:
        schedule.run_pending()
        threading.Event().wait(43200)
        print(1)
#   Повторение обновления времени в Х часов

schedule.every().day.at("00:00").do(updatetime)

#   Создания бота

bot = commands.Bot(command_prefix='!')

#   Команда для вывода ключа сервера

@bot.command(name = "checkkey")
async def checkkey(ctx,arg):
    if arg == 1 and ctx.guild.id == 548223779705323520:
        cur.execute("SELECT * FROM clientservers")
        rez = cur.fetchall()
        await me.send(rez)
    elif ctx.guild.id == 548223779705323520 and arg !=1:
        cur.execute("SELECT * FROM clientservers WHERE servername = ?",(arg,))
        rez = cur.fetchall()
        await me.send(rez)

#   Команда для присвоения приватного статуса серверу

@bot.command(name = "payinf")
async def payinf(ctx,arg1,arg2,arg3):
    if ctx.guild.id == 548223779705323520:
        print(1)
        if arg1 == -2:
            cur.execute("UPDATE clientservers set payinfo = ? WHERE serverid = ?", (arg1, arg2,))
        else:
            cur.execute("SELECT * FROM clientservers WHERE serverid = ?", (arg2,))
            restm = cur.fetchone()
            cur.execute("UPDATE clientservers set payinfo = ?,time = ? WHERE serverid = ?",(arg1,restm[3]+int(arg3),arg2))
        connect.commit()

#   Команда для ввода ключа

@bot.command(name = "keyuse")
async def keyuse(ctx,arg):
    id = ctx.guild.id
    cur.execute("SELECT * FROM clientservers WHERE serverid = ?",(id,))
    rez = cur.fetchone()
    print(rez)
    if arg == rez[4]:
        cur.execute("UPDATE clientservers set time = ?,onemonth = ? WHERE serverid = ?",(720+rez[3],keycreate(),ctx.guild.id,))
        connect.commit()
    if arg == rez[5]:
        cur.execute("UPDATE clientservers set time = ?,threemonth = ? WHERE serverid = ?",(2160+rez[3],keycreate(),ctx.guild.id,))
        connect.commit()
    print(ctx.guild.id)

#   Проверка запуска бота

@bot.event
async def on_ready():
    global me
    print("we have {0.user}".format(bot))
    print(len(bot.guilds))
    me = discord.utils.get(bot.get_all_channels(), guild__name='Боги из 2002', name="тест")
    print(me)

#   Ивент с добавлением сервера

@bot.event
async def on_guild_join(guild):
    cur.execute("SELECT * FROM clientservers WHERE serverid = ?", (guild.id,))
    rez = cur.fetchone()
    if rez == None:
        t = time.localtime()
        t = t[3]+1
        onemonthkey = keycreate()
        threemonthkey = keycreate()
        clientserver = (f"{guild.name}",f"{guild.id}","0","76",f"{t}",f"{onemonthkey}",f"{threemonthkey}")
        cur.execute("INSERT INTO clientservers VALUES(?,?,?,?,?,?,?)",clientserver)
        #74
        connect.commit()
        await discord.utils.get(bot.get_all_channels(), guild__name='Боги из 2002', name="servers").send(guild.name+f" {onemonthkey} "+ f"{threemonthkey}")

#   Ивент при отправке сообщения

@bot.event
async def on_message(message):
    t0 = time.time()
    cur.execute("SELECT * FROM clientservers WHERE serverid = ?",(message.guild.id,))
    servres = cur.fetchone()
    #print(type(servres[2]))
    if servres[3]>0 or servres[2]== -1:
        if isinstance(message.content,str) and str(message.author) != "NN _ antimat#0525":
            #print(message.guild.name)
            messageres = message.content
            countlet = 0
            messageres = n_gramm(messageres)
            #if len(messageres)> 100
            filter = {'}|{': 'ж', 'IO': 'ю', 'a': 'а', 'A': 'а', 'o': 'о', 'O': 'о', 'b': 'б', 'B': 'в', 'r': 'р',
                      'g': 'г',
                      'd': 'д', 'E': 'е', 'e': 'е',
                      'z': 'з', '3': 'з', 'N': 'n', 'k': 'к', 'K': 'к', 'L': 'л', 'M': 'м', 'H': 'н', 'n': 'н',
                      'p': 'п',
                      'P': 'п', 'c': 'с', 'C': 'с',
                      'T': 'т', 'm': 'м', 't': 'т', 'y': 'у', 'Y': 'у', 'x': 'х', 'X': 'х', 'u': 'ц', '4': 'ч',
                      'w': 'ш',
                      'W': 'ш', 'R': 'r', 'i': 'и', '1': 'и', '@': 'а', 'I': 'и', }
            #for f in filter:
                #messageres = messageres.replace(f, filter[f])
            print(messageres)
            sen_res = matmassage(messageres)
            if sen_res > 0.5:
                await message.delete()
                t2 = time.time()
                t2 = t2 - t0
                channel = message.channel
                embed = discord.Embed(
                    title='Ваше сообщение удалено,так как оно содержит незензурную лексику,а это запрещено правилами канала',)
                await channel.send(embed = embed)

                print("Время удаления : ", t2)
                #await me.send(1)
                await me.send("1;"+ message.content + f" {round(t2,3)}")
            else:
                #await me.send("0;" + message.content)
                pass
            await bot.process_commands(message)
            #t1 = time.time()

#   Создание второго потока для проверки времени

thread2 = Thread(target=runtime)
#thread1 = Thread(target=on_message,args = (message))
thread2.start()

#   Запускаем бота

bot.run("OTA0NDA3MDU2OTk0NDE0NjEy.YX7EtQ.de8fALQnYKb1o5opN2TUKFI1NKA")
