# ======================================= Развлечения
import requests
import bs4  # BeautifulSoup4
from telebot import types
from io import BytesIO
import SECRET  # секретные ключи, пароли
import random
import hor
import datetime


# -----------------------------------------------------------------------
def get_text_messages(bot, message, update, context):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Прислать собаку":
        bot.send_photo(chat_id, photo=get_dogURL(), caption="Вот тебе собачка!")

    elif ms_text == "Прислать лису":
        bot.send_photo(chat_id, photo=get_foxURL(), caption="Вот тебе лисичка!")

    elif ms_text == "Прислать анекдот":
        bot.send_message(chat_id, text=get_anekdot())

    # elif ms_text == "Прислать новости":
    #    bot.send_message(chat_id, text=get_news())

    elif ms_text == "Прислать фильм":
        send_film(bot, chat_id)

    elif ms_text == "Угадай кто?":
        get_ManOrNot(bot, chat_id)

    # elif ms_text == "Прислать курсы":
    #     bot.send_message(chat_id, text=get_cur())

    elif ms_text == 'Орел или решка':
        head_or_tail(bot, chat_id)

    # elif ms_text == 'Agario':
    #     start_hor(bot, chat_id, update, context)

    elif ms_text == 'Узнать правду':
        gay_or_not(bot, chat_id)


# -----------------------------------------------------------------------
def send_film(bot, chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)


# -----------------------------------------------------------------------
def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.anekdot_text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""


# -----------------------------------------------------------------------
def get_foxURL():
    url = ""
    req = requests.get('https://randomfox.ca/floof/')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['image']
        # url.split("/")[-1]
    return url


# -----------------------------------------------------------------------
def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
        # url.split("/")[-1]
    return url


# -----------------------------------------------------------------------
def get_ManOrNot(bot, chat_id):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить",
                                      url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")


# ---------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm


# ---------------------------------------------------------------------
def head_or_tail(bot, chat_id):
    m = random.randint(0, 1)
    if m == 0:
        bot.send_message(chat_id, text='Выпала решка!')
    else:
        bot.send_message(chat_id, text='Выпал орел!')


# ---------------------------------------------------------------------
def gay_or_not(bot, chat_id):
    bot.send_message(chat_id,
                     text=f'Привет. Здесь ты узнаешь, насколько процентов ты похож на голубое небо.')
    m = random.randint(0, 100)
    if m == 0:
        bot.send_message(chat_id, text=f'С ума сойти, ты 100% натурал')
    elif m == 50:
        bot.send_message(chat_id, text=f'Ты золотая середина, 50%')
    elif m == 100:
        bot.send_message(chat_id,
                         text=f'Поздравляем, голубее вас только небо. Держите медальку за 100%!')
    else:
        bot.send_message(chat_id, text=f'Bаш результат - {m}%')


# ------------------------------------------------------------------------------------------------

STATE = None
BIRTH_YEAR = 1
BIRTH_MONTH = 2
BIRTH_DAY = 3


def start_hor(bot, chat_id, update, context):
    bot.send_message(chat_id, f"Мне нужна некоторые данные о вас, чтобы подобрать гороскоп")
    start_getting_birthday_info(update, context, chat_id, bot)


def start_getting_birthday_info(update, context, chat_id, bot):
    global STATE
    STATE = BIRTH_YEAR
    bot.send_message(chat_id, f"В каком году вы родились (2003, 1978, 1670...)?")
    received_birth_year(update, context, bot, chat_id)


def received_birth_year(update, context, bot, chat_id):
    global STATE
    try:
        today = datetime.date.today()
        year = int(update.message.text)
        if year > today.year:
            raise ValueError("неверное значение")
        context.user_data['birth_year'] = year
        bot.send_message(chat_id, f"Напишите месяц своего рождения (декабрь - 12, ноябрь - 11 и т. д.)")
        STATE = BIRTH_MONTH
        received_birth_month(update, context, bot, chat_id)
    except:
        update.message.reply_text(
            "неверное значение")


def received_birth_month(update, context, bot, chat_id):
    global STATE
    try:
        month = int(update.message.text)
        if month > 12 or month < 1:
            raise ValueError("неверное значение")
        context.user_data['birth_month'] = month
        bot.send_message(chat_id, f"Отлично! Остался только день")
        STATE = BIRTH_DAY
        received_birth_day(update, context, bot, chat_id)
    except:
        bot.send_message(chat_id, "неверное значение")


def received_birth_day(update, context, bot, chat_id):
    global STATE
    try:
        today = datetime.date.today()
        dd = int(update.message.text)
        yyyy = context.user_data['birth_year']
        mm = context.user_data['birth_month']
        birthday = datetime.date(year=yyyy, month=mm, day=dd)
        if today - birthday < datetime.timedelta(days=0):
            raise ValueError("неверное значение")
        context.user_data['birthday'] = birthday
        STATE = None
        bot.send_message(chat_id, f'Итак, вы родились {birthday}')
    except:
        bot.send_message(chat_id, "неверное значение")


def text(update, context, bot, chat_id):
    global STATE
    if STATE == BIRTH_YEAR:
        return received_birth_year(update, context, bot, chat_id)
    if STATE == BIRTH_MONTH:
        return received_birth_month(update, context, bot, chat_id)
    if STATE == BIRTH_DAY:
        return received_birth_day(update, context, bot, chat_id)


def hor_send(update, context, sign, user_hor_text):
    calculate_zodiac(context.user_data['birthday'])
    update.message.reply_text(f"Ваш знак зодиака: {sign}")
    update.message.reply_text(f"Ваш гороскоп:\n {user_hor_text}")


def calculate_zodiac(birthdate):
    import pyaztro

    m = birthdate.month
    d = birthdate.day

    if m == 12:
        sign = 'sagittarius' if (d < 22) else 'capricorn'
    elif m == 1:
        sign = 'capricorn' if (d < 20) else 'aquarius'
    elif m == 2:
        sign = 'aquarius' if (d < 19) else 'pisces'
    elif m == 3:
        sign = 'pisces' if (d < 21) else 'aries'
    elif m == 4:
        sign = 'aries' if (d < 20) else 'taurus'
    elif m == 5:
        sign = 'taurus' if (d < 21) else 'gemini'
    elif m == 6:
        sign = 'gemini' if (d < 21) else 'cancer'
    elif m == 7:
        sign = 'cancer' if (d < 23) else 'leo'
    elif m == 8:
        sign = 'leo' if (d < 23) else 'virgo'
    elif m == 9:
        sign = 'virgo' if (d < 23) else 'libra'
    elif m == 10:
        sign = 'libra' if (d < 23) else 'scorpio'
    elif m == 11:
        sign = 'scorpio' if (d < 22) else 'sagittarius'

    user_hor = pyaztro.Aztro(sign=sign)
    user_hor_text = sign.description
