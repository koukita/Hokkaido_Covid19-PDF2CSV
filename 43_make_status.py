import os
import csv
import pandas as pd
import numpy as np
import file_day
import pdf_download_path
from datetime import datetime, date, timedelta
import shutil
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN #四捨五入するためのライブラリ

#昨日の日付
dt_mmdd_yday = file_day.f_yesterday()
dt_mmdd_today = file_day.f_today()
print("今日は" + dt_mmdd_today)
d_year = datetime.today().year
d_month = datetime.today().month
today = int(dt_mmdd_today[-2:])

#CSVのフォルダを指定
download_path = pdf_download_path.p_path()
covid19_path = pdf_download_path.covid_path()

#ファイルが存在するか確認
if(os.path.exists(covid19_path + "\\hokkaido_03status_day.csv")) and (os.path.exists(download_path + "\\day_total_status_" + dt_mmdd_today + ".csv")):
    #pandasでCSVファイルを読み込み
    df_covid19 = pd.read_csv(covid19_path + "\\hokkaido_03status_day.csv", encoding="CP932")
    df_total = pd.read_csv(download_path + "\\day_total_status_" + dt_mmdd_today + ".csv", encoding="CP932")
    df_hokkaido = pd.read_csv(download_path + "\\day_hokkaido_status_" + dt_mmdd_today + ".csv", encoding="CP932")

    #最新の日付を確認
    kei_day = str(df_covid19.iloc[len(df_covid19)-1,0])

    #今日の日付
    today_day = file_day.txt_day()
    print(today_day)

    #ファイルをバックアップする
    shutil.copyfile(covid19_path + "\\hokkaido_03status_day.csv", covid19_path + "\\backup\\hokkaido_03status_day_backup" + dt_mmdd_today + ".csv")

    if today_day == kei_day: #最新の日付が今日の日付か確認
        print("すでに今日のデータがあります。プログラムを終了します。")
    else:
        num_total = df_total.values[0] #データを配列で取得
        list_total = num_total.tolist() #NumPy配列ndarrayをリストに変換
        list_total.insert(0,today_day) #日付の挿入
        
        #北海道のみのデータをリストにする
        num_hokkaido = df_hokkaido.values[0] #データを配列で取得
        list_hokkaido = num_hokkaido.tolist() #NumPy配列ndarrayをリストに変換
        #不要な要素を削除
        del list_hokkaido[:2]
        del list_hokkaido[5]
        list_hokkaido.insert(0,today_day) #日付の挿入
        #print(list_hokkaido)

        #追加用リストの作成
        list_total =list_total + [""] + list_hokkaido + [""]
        tmp_se = pd.Series(list_total, index=df_covid19.columns)

        #今日のデータを追加しCSVに保存
        tmp_se = pd.Series(list_total, index=df_covid19.columns)
        df_covid19 = df_covid19.append(tmp_se, ignore_index = True)
        print("状態ごとの日計の合計＝" + str(df_covid19["日計"].sum()))
        df_covid19.to_csv(covid19_path + "\\自動作成ファイル\\hokkaido_03status_day.csv",index=None,header=True, encoding="CP932")
else:
    print("【状態ごと】必要なファイルがない")


