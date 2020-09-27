from celery import Celery
from celery.schedules import timedelta
from decouple import config
import random
import custom_utils
from peewee import SqliteDatabase, Model, CharField, PrimaryKeyField
# import requests
# from bs4 import BeautifulSoup
from pyrogram import Client, InlineKeyboardMarkup, InlineKeyboardButton


url = config('REDIS_URL')
app = Celery('main', broker=url)
app.conf.timezone = 'Europe/Kiev'
app.conf.beat_schedule = {
    'send_film': {
        'task': 'task.film',
        'schedule': timedelta(hours=1)
    }
}


database = SqliteDatabase('films.sqlite3')
database.connect()

class Film(Model):
    id = PrimaryKeyField()
    url = CharField(max_length=250)
    class Meta:
        database = database


@app.task
def film():
    app = Client(
        'filmy_bot',
    api_id = '1319289' ,
    api_hash = '8f5127ed38135aa349a7384f547a309c' ,
    bot_token = '1263380136:AAG_kErZYKbrBNxpZzxcOlTo32ffLHQOaJQ' ,
    )
    choose = random.randint(1, len(Film.select()))
    film = Film.get_by_id(choose)
    ans = custom_utils.parsing(film.url)
    with app:
       app.send_message(
            'filmy',
            ans[0],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('🎥 Смотреть онлайн!', url=ans[1])],
                [InlineKeyboardButton('🔎 Поиск фильмов!', url='http://w.ikino.site/index.php?do=search')]
            ]),
        )
    Film.delete_by_id(choose)

# print(Film.get_by_id(1))
# for i in Film.select():
#     print(i)
# Film.create_table()

# for i in range(1, 516):
#     page = requests.get(f'http://f2.ikino.site/filmy/page/{i}/')
#     soup = BeautifulSoup(page.text, 'html.parser')
#     films = soup.find(
#         'div', {
#             'id': 'dle-content'
#             }
#     ).find_all(
#         'article', {
#             'class': 'movie-box'
#         }
#     )
#     for x in films:
#         year = x.find(
#             'div', {
#                 'class': 'metadata'
#             }
#         ).find(
#             'span'
#         ).text
#         if int(year) < 2000:
#             continue
#         try:
#             imdb = x.find(
#                 'div', {
#                     'class': 'rate'
#                 }
#             ).find(
#                 'span'
#             ).text
#             if not float(imdb) > 5.0:
#                 continue
#         except:
#             try:
#                 kp = x.find(
#                     'div', {
#                         'class': 'rate-kp'
#                     }
#                 ).find(
#                     'span'
#                 ).text
#                 if not float(kp) > 5.0:
#                     continue
#             except:
#                 continue
#         link = x.find(
#             'a'
#         ).get(
#             'href'
#         )
#         Film.create(
#             url=link
#         )
#         print(i, Film.get(Film.url == link))
#         print(i, Film.get(Film.url == link).url)

