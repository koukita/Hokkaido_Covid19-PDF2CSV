import os
from datetime import datetime, date, timedelta

#今日の日付計算
def f_today():
    now_time = int(datetime.strftime(datetime.now(),'%H'))
    today = datetime.today()
    if now_time < 8: #朝8時より前なら前日にする
        today = today - timedelta(days=1)

    c_mmdd = datetime.strftime(today,'%m%d')
    return c_mmdd

#昨日の日付計算
def f_yesterday():
    now_time = int(datetime.strftime(datetime.now(),'%H'))
    today = datetime.today()
    if now_time < 8: #朝8時より前なら前日にする
        yesterday = today - timedelta(days=2)
    else:
        yesterday = today - timedelta(days=1)
        
    c_mmdd = datetime.strftime(yesterday,'%m%d')
    return c_mmdd

def long_txt_day():
    now_time = int(datetime.strftime(datetime.now(),'%H'))
    today = datetime.today()
    if now_time < 8: #朝8時より前なら前日にする
        today = today - timedelta(days=1)

    c_mmdd = datetime.strftime(today,'%Y-%m-%dT00:00')
    return c_mmdd

def txt_day():
    now_time = int(datetime.strftime(datetime.now(),'%H'))
    today = datetime.today()
    if now_time < 8: #朝8時より前なら前日にする
        today = today - timedelta(days=1)

    c_mmdd = datetime.strftime(today,'%Y-%m-%d')
    return c_mmdd


