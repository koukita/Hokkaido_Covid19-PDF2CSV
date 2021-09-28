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
if(os.path.exists(covid19_path + "\\hokkaido_05hospitalization_day.csv")) and (os.path.exists(download_path + "\\day_hokkaido_nyuin_" + dt_mmdd_yday + ".csv")):
    #pandasでCSVファイルを読み込み
    df_covid19 = pd.read_csv(covid19_path + "\\hokkaido_05hospitalization_day.csv", encoding="CP932")
    df_total = pd.read_csv(download_path + "\\day_hokkaido_nyuin_" + dt_mmdd_yday + ".csv", encoding="CP932")

    #最新の日付を確認
    kei_day = str(df_covid19.iloc[len(df_covid19)-1,0])

    #今日の日付
    yday_day = file_day.txt_yesterday()
    print(yday_day)

    #ファイルをバックアップする
    shutil.copyfile(covid19_path + "\\hokkaido_05hospitalization_day.csv", covid19_path + "\\backup\\hokkaido_05hospitalization_day_backup" + dt_mmdd_yday + ".csv")

    if yday_day == kei_day: #最新の日付が今日の日付か確認
        print("すでに昨日のデータがあります。プログラムを終了します。")
    else:
        num_total = df_total.values[0] #データを配列で取得
        list_total = num_total.tolist() #NumPy配列ndarrayをリストに変換
        list_total.insert(0,yday_day) #日付の挿入
        tmp_se = pd.Series(list_total, index=df_covid19.columns)
        print("合計の確認：現在患者数＝" + str(list_total[1]) + "人")
        print("　　　　　その他の合計＝" + str(list_total[3] + list_total[5] + list_total[7] + list_total[9] + list_total[11]) + "人　同じならOK" )
        df_covid19 = df_covid19.append(tmp_se, ignore_index = True)
        df_covid19.to_csv(covid19_path + "\\自動作成ファイル\\hokkaido_05hospitalization_day.csv",index=None,header=True, encoding="CP932")

        #「.0」を削除（置き換え） 参考にしたサイト【https://www.teihenai.com/2018/11/29/python-chikan/】
        fn = covid19_path + "\\自動作成ファイル\\hokkaido_05hospitalization_day.csv"
        #ファイル読み込み
        with open(fn, "r") as f:
            s = f.read()
        #文字を置き換え
        s = s.replace(".0","")
        #ファイルを保存
        with open(fn, "w") as f:
            f.write(s)

else:
    print("【入院属性】必要なファイルがない")


