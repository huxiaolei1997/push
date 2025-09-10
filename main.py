import os
import math
import random
import requests
import datetime

from zhdate import ZhDate
from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate

today = datetime.now()

# 微信公众测试号ID和SECRET
app_id = 'wxab190723497fc82b'
app_secret = 'c14d943f9bcd752943c1d10fc6b60776'

# 可把os.environ结果替换成字符串在本地调试
# user_ids = os.environ["USER_ID"].split(',')
# template_ids = os.environ["TEMPLATE_ID"].split(',')
# citys = os.environ["CITY"].split(',')
# solarys = os.environ["SOLARY"].split(',')
# start_dates = os.environ["START_DATE"].split(',')
# birthdays = os.environ["BIRTHDAY"].split(',')
# onbfH6vz6u3fWReh0wPjfAdny2yw
# onbfH6lJGju2dBhqfmKhk_nzELIk
user_ids = 'onbfH6vz6u3fWReh0wPjfAdny2yw'.split(',')
# template_ids = 'E81x2iNPpVBRtKiIt_ldKr9Dn_Hi24-XCkUuPmzf_pk'.split(',')
template_id_configs = {
    "0518": "a5qcj3Be31BJN4bemOPCRblIfYqEZIwrg1Dt57K-gaU",
    "0520": "gcIMVKeKyGWIYfCfys9E9eHiGrimzfm68VW3Ak_EzAk",
    "0416": "379LvHbWCa3SPBt1XYKrERfwXOq4Cm4jd0pdMXjfeok",
    "0214": "XpTEWBC2LbLAqYexmPfag7lb43VDd3Cf8jVIckPBoYQ",
    "normal": "E81x2iNPpVBRtKiIt_ldKr9Dn_Hi24-XCkUuPmzf_pk",
    "qixi": "MKG5ioCuKaQ6zQ9ZxsLJw07BUnKaJ6rHBw1cTFR08fw",
    "0826": "-PRXxHOGsAB629taLdrCdehanMhB5qW9YA6pXgdZ14U",
}
template_ids = 'E81x2iNPpVBRtKiIt_ldKr9Dn_Hi24-XCkUuPmzf_pk'.split(',')
citys = '330108'.split(',')
start_dates = '2025-05-18'.split(',')
birthdays = '04-16'.split(',')


client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

def is_qixi(check_date):
    """判断给定日期是否为七夕节"""
    # 处理字符串类型的日期
    if isinstance(check_date, str):
        try:
            check_date = datetime.strptime(check_date, "%Y-%m-%d")
        except ValueError:
            # 如果是"MMDD"格式的字符串
            try:
                check_date = datetime.strptime(str(date.today().year) + "-" + check_date, "%Y-%m-%d")
            except ValueError:
                return False

    try:
        lunar_date = ZhDate.from_datetime(check_date)
        return lunar_date.lunar_month == 7 and lunar_date.lunar_day == 7
    except:
        return False

# 获取天气和温度
def get_weather(city):
    url = "https://restapi.amap.com/v3/weather/weatherInfo?key=31a3754cb9daaf678f8e972bf3dea5cc&city=" + city + "&extensions=base&output=json"
    res = requests.get(url).json()
    weather = res['lives'][0]
    return weather['weather'], weather['temperature_float'], weather['city']


def get_city_date(city):
    return city, today.date().strftime("%Y-%m-%d")

def get_city_date_v2():
    return today.date(), today.date().strftime("%m%d")
    # return today.date(), '0826'
    # return datetime.strptime('2025-08-29', "%Y-%m-%d"), '0829'


def get_count(start_date):
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days



def calculate_age_simple(birth_date_str):
    # 解析出生日期
    year, month, day = map(int, birth_date_str.split('-'))
    birth_date = date(year, month, day)
    # 当前日期
    today = date.today()
    # 计算年龄
    age = today.year - birth_date.year
    if today < birth_date.replace(year=today.year):
        age -= 1
    return age

def get_birthday(birthday):
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

def sendBirthdayPush(currentDateStr, user_id):
    age = calculate_age_simple('2001-04-16')
    data = {
        "age": {"value": "{}".format(age), "color": get_random_color()}
    }
    wm.send_template(user_id, template_id_configs[currentDateStr], data)

def send100Push(currentDateStr, user_id):
    data = {
        "today": {"value": "{}".format(today.date().strftime("%Y年%-m月%-d号")), "color": get_random_color()}
    }
    wm.send_template(user_id, template_id_configs[currentDateStr], data)

def send0520Push(currentDateStr, user_id):
    data = {}
    wm.send_template(user_id, template_id_configs[currentDateStr], data)

def send0214Push(currentDateStr, user_id):
    data = {}
    wm.send_template(user_id, template_id_configs[currentDateStr], data)

def send0518Push(currentDateStr, user_id):
    data = {
        "love_days": {"value": "{}".format(get_count(start_dates[i])), "color": get_random_color()}
    }
    wm.send_template(user_id, template_id_configs[currentDateStr], data)


def sendQixiPush(currentDateStr, user_id):
    data = {
        "love_days": {"value": "{}".format(get_count(start_dates[i])), "color": get_random_color()}
    }
    wm.send_template(user_id, template_id_configs[currentDateStr], data)


def sendNormalPush(currentDateStr, user_id):
    wea, tem, city_name = get_weather(citys[0])
    cit, dat = get_city_date(citys[0])
    data = {
        "date": {"value": "{}".format(dat), "color": get_random_color()},
        "city": {"value": "{}".format(city_name), "color": get_random_color()},
        "weather": {"value": "{}".format(wea), "color": get_random_color()},
        "temperature": {"value": "{}".format(tem), "color": get_random_color()},
        "birthday_left": {"value": "{}".format(get_birthday(birthdays[i])), "color": get_random_color()},
        "love_days": {"value": "{}".format(get_count(start_dates[i])), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}
    }
    wm.send_template(user_id, template_id_configs['normal'], data)


for i in range(len(user_ids)):
    currentDate, currentDateStr = get_city_date_v2()
    user_id = user_ids[i]
    if currentDateStr == "0214":
        send0214Push(currentDateStr, user_id)
    elif currentDateStr == "0416":
        sendBirthdayPush(currentDateStr, user_id)
    elif currentDateStr == "0518":
        send0518Push(currentDateStr, user_id)
    elif currentDateStr == "0520":
        send0520Push(currentDateStr, user_id)
    elif currentDateStr == "0826":
        send100Push(currentDateStr, user_id)
    elif is_qixi(datetime.strftime(currentDate, "%m-%d")):
        sendQixiPush("qixi", user_id)
    else:
        sendNormalPush(currentDateStr, user_id)

# 七夕、2.14、4.16、5.20、5.18
