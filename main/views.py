# -*- coding: utf-8 -*-
from main.models import DailyFood
from django.shortcuts import render
from django.http import JsonResponse
from ipware import get_client_ip
from django.conf import settings
import requests
import openai
import datetime
import json
import re
import os

openai.api_key = settings.OPENAI_API_KEY

def index(request):
    content = {}
    return render(request, 'index.html', content)


def get_eatgpt(request):
    n = 0
    food_dict = {}
    client_ip, is_routable = get_client_ip(request)
    client_ip = '123.123.123.123' if client_ip == '127.0.0.1' else client_ip
    # 百度IP归属地查询
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query=%s&co=&resource_id=6006&t=1529809984888&ie=utf8&oe=gbk&format=json&tn=baidu'%client_ip
    response = requests.get(url).json()
    city = response['data'][0]['location'].split(' ')[0]
    # 日期
    date = datetime.datetime.now().strftime("%m月%d日")

    # 是否重复查询
    daily_food_by_date_and_ip = DailyFood.objects.filter(date='%s'%date, ip='%s'%client_ip)
    if not daily_food_by_date_and_ip:
        n = 0
    else:
        n = 9999
        food_dict = daily_food_by_date_and_ip.last().food_dict.replace("'", '"')
        food_dict = json.loads(food_dict)

    def put_database(client_ip, date, food_dict, food):
        daily = DailyFood(ip='%s'%client_ip, date='%s'%date, food_dict='%s'%food_dict, raw='%s'%food)
        daily.save()

    # 循环调用openai，防止响应格式有误
    while n < 5:
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "假如你是一个中餐厨师"},
                {"role": "user", "content": """今天%s，我在%s，请谨慎严选冷菜二道，热菜三道可以有肉，特色菜两道，请严格按照菜品数量，且都是适合今天吃的菜，说明理由，并且严格按照这个格式：
                                                冷菜：
                                                菜名：简短介绍
                                                热菜：
                                                菜名：简短介绍
                                                特色菜
                                                菜名：简短介绍"""%(date, city)},
            ]
        )
        food = completion.choices[0].message['content']

        # 匹配重组为字典
        food_list = re.findall(r'[1-9]\. (.*)。', food)
        for i in food_list:
            food_dict['%s'%i.split('：')[0]] = i.split('：')[1]

        # 匹配不到时匹配下一个规则    
        if not food_dict:
            pass
        else:
            put_database(client_ip, date, food_dict, food)
            break

        food_name_list = re.findall(r'菜名：(.*)', food)
        food_info_list = re.findall(r'(?:简短介绍|简介|介绍)：(.*)', food)
        for i in range(0, len(food_name_list)):
            food_dict['%s'%food_name_list[i]] = food_info_list[i]

        if not food_dict:
            pass
        else:
            put_database(client_ip, date, food_dict, food)
            break


    return JsonResponse(food_dict, safe=False)
