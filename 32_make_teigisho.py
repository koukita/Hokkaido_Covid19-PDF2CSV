import os
import sys
import csv
import pandas as pd
import file_day
import pdf_download_path
from datetime import datetime, date, timedelta
import shutil

#昨日の日付
today = datetime.today()
dt_mmdd_yday = file_day.f_yesterday()
dt_mmdd_today = file_day.f_today()
print("今日は" + dt_mmdd_today)

#CSVのフォルダを指定
download_path = pdf_download_path.p_path()
covid19_path = pdf_download_path.covid_path()

#ファイルが存在するか確認
if(os.path.exists(covid19_path + "\\010006_hokkaido_covid19_patients.csv")) and (os.path.exists(download_path + "\\csv_merge_" + dt_mmdd_today + ".csv")):
    #pandasでCSVファイルを読み込み
    df_patients = pd.read_csv(covid19_path + "\\010006_hokkaido_covid19_patients.csv", encoding="CP932")
    df_csv_merge = pd.read_csv(download_path + "\\csv_merge_" + dt_mmdd_today + ".csv", encoding="CP932")

    #一番最後の行を確認し、今日の日付なら終了
    last_day = str(df_patients.iloc[len(df_patients)-1,4])
    #今日の日付
    today_day = file_day.txt_day()
    if today_day == last_day:
        print("すでに今日のデータがあります。プログラムを終了します。")
        sys.exit()

    #ファイルをバックアップする
    shutil.copyfile(covid19_path + "\\010006_hokkaido_covid19_patients.csv", covid19_path + "\\backup\\010006_hokkaido_covid19_patient_backup" + dt_mmdd_today + ".csv")

    #今日のデータを追加
    for gyou_today in range(0,len(df_csv_merge)):
        p_No = str(df_csv_merge.iloc[gyou_today,0]) #No
        p_code = "10006"
        p_pref = "北海道"
        p_day = file_day.txt_day() #公表_年月日
        p_hasshoubi = str(df_csv_merge.iloc[gyou_today,9]) #公表_発症日
        p_kyojyu = str(df_csv_merge.iloc[gyou_today,3]) #患者_居住地
        p_age = str(df_csv_merge.iloc[gyou_today,1]) #患者_年代
        p_sex = str(df_csv_merge.iloc[gyou_today,2]) #患者_性別
        p_job = str(df_csv_merge.iloc[gyou_today,4]) #患者_職業
        p_jyoutai = str(df_csv_merge.iloc[gyou_today,5]) #患者_状態
        p_shoujyou = str(df_csv_merge.iloc[gyou_today,11]) #患者_症状
        p_tokou = str(df_csv_merge.iloc[gyou_today,12]) #渡航履歴
        print(p_No +  str(df_csv_merge.iloc[gyou_today,7]))
        if str(df_csv_merge.iloc[gyou_today,7]) == "1":
            p_saiyousei = 1
        else:
            p_saiyousei = 0

        p_bikou = str(df_csv_merge.iloc[gyou_today,13]) #備考

        #配列を作る
        p_array =[p_No, p_code, p_pref, "", p_day, p_hasshoubi, p_kyojyu, p_age, p_sex, p_job, p_jyoutai, p_shoujyou, p_tokou, p_saiyousei, "", p_bikou ]
        #リストを検索し、「nan」を空白に置き換え
        for index,value in enumerate(p_array):
            if value == "nan":
                p_array[index] = ""

        tmp_se = pd.Series(p_array, index=df_patients.columns)
        df_patients = df_patients.append(tmp_se, ignore_index = True)
        print(p_array)

    df_patients.to_csv(covid19_path + "\\自動作成ファイル\\010006_hokkaido_covid19_patients.csv", index=None, encoding='CP932')
else:
    print("必要なファイルがない")


