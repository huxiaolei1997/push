import os
import math
import random
import requests

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

user_ids = 'onbfH6vz6u3fWReh0wPjfAdny2yw'.split(',')
template_ids = 'E81x2iNPpVBRtKiIt_ldKr9Dn_Hi24-XCkUuPmzf_pk'.split(',')
citys = '330108'.split(',')
start_dates = '2025-05-18'.split(',')
birthdays = '04-16'.split(',')

# 获取天气和温度
def get_weather(city):
    url = "https://restapi.amap.com/v3/weather/weatherInfo?key=31a3754cb9daaf678f8e972bf3dea5cc&city=" + city + "&extensions=base&output=json"
    res = requests.get(url).json()
    weather = res['lives'][0]
    return weather['weather'], weather['temperature_float'], weather['city']


# 当前城市、日期
def get_city_date(city):
    return city, today.date().strftime("%Y-%m-%d")


# 距离设置的日期过了多少天
def get_count(start_date):
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


# 距离发工资还有多少天
def get_solary(solary):
    next = datetime.strptime(str(date.today().year) + "-" + str(date.today().month) + "-" + solary, "%Y-%m-%d")
    if next < datetime.now():
        if next.month == 12:
            next = next.replace(year=next.year + 1)
        next = next.replace(month=(next.month + 1) % 12)
    return (next - today).days


# 距离过生日还有多少天
def get_birthday(birthday):
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


# 每日一句
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


# 字体随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

for i in range(len(user_ids)):
    wea, tem, city_name = get_weather(citys[i])
    cit, dat = get_city_date(citys[i])
    data = {
        "date": {"value": "{}".format(dat), "color": get_random_color()},
        "city": {"value": "{}".format(city_name), "color": get_random_color()},
        "weather": {"value": "{}".format(wea), "color": get_random_color()},
        "temperature": {"value": "{}".format(tem), "color": get_random_color()},
        "birthday_left": {"value": "{}".format(get_birthday(birthdays[i])), "color": get_random_color()},
        "love_days": {"value": "{}".format(get_count(start_dates[i])), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}
    }
    res = wm.send_template(user_ids[i], template_ids[i], data)
    print(res)
