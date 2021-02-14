import os
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
if(os.path.exists(covid19_path + "\\patients_age_sex.csv")) and (os.path.exists(download_path + "\\csv_merge_" + dt_mmdd_today + ".csv")):
    #pandasでCSVファイルを読み込み
    df_patients = pd.read_csv(covid19_path + "\\patients_age_sex.csv", encoding="CP932")
    df_csv_merge = pd.read_csv(download_path + "\\csv_merge_" + dt_mmdd_today + ".csv", encoding="CP932")

    #前日までの合計を取得
    kei_day = str(df_patients.iloc[len(df_patients)-1,0])
    kei_20 = str(df_patients.iloc[len(df_patients)-1,1])
    kei_40 = str(df_patients.iloc[len(df_patients)-1,2])
    kei_60 = str(df_patients.iloc[len(df_patients)-1,3])
    kei_80 = str(df_patients.iloc[len(df_patients)-1,4])
    kei_100 = str(df_patients.iloc[len(df_patients)-1,5])
    kei_age_null = str(df_patients.iloc[len(df_patients)-1,6])
    kei_man = str(df_patients.iloc[len(df_patients)-1,7])
    kei_woman = str(df_patients.iloc[len(df_patients)-1,8])
    kei_sex_null = str(df_patients.iloc[len(df_patients)-1,9])

    today_20 = int(kei_20)
    today_40 = int(kei_40)
    today_60 = int(kei_60)
    today_80 = int(kei_80)
    today_100 = int(kei_100)
    today_age_null = int(kei_age_null)
    today_man = int(kei_man)
    today_woman = int(kei_woman)
    today_sex_null = int(kei_sex_null)

    #今日の日付
    today_day = file_day.long_txt_day()
    if today_day == kei_day:
        print("すでに今日のデータがあります。プログラムを終了します。")
    else:
        #ファイルをバックアップする
        shutil.copyfile(covid19_path + "\\patients_age_sex.csv", covid19_path + "\\backup\\patients_age_sex_backup" + dt_mmdd_today + ".csv")

        #今日のデータを追加
        for gyou_today in range(0,len(df_csv_merge)):
            p_No = str(df_csv_merge.iloc[gyou_today,0]) #No
            p_age = str(df_csv_merge.iloc[gyou_today,1]) #年代
            #年齢のグループ
            if p_age == "10歳未満" or p_age == "10代" or p_age == "20代":
                today_20 = today_20 + 1
            elif p_age == "30代" or p_age == "40代":
                today_40 = today_40 + 1
            elif p_age == "50代" or p_age == "60代":
                today_60 = today_60 + 1
            elif p_age == "70代" or p_age == "80代":
                today_80 = today_80 + 1
            elif p_age == "90代" or p_age == "100代":
                today_100 = today_100 + 1
            else:
                today_age_null = today_age_null + 1
            
            p_sex = str(df_csv_merge.iloc[gyou_today,2]) #性別
            #性別
            if p_sex == "男性":
                today_man = today_man + 1
            elif p_sex == "女性":
                today_woman = today_woman + 1
            else:
                today_sex_null = today_sex_null + 1

        
        #配列を作る
        p_array =[today_day, today_20, today_40, today_60, today_80, today_100, today_age_null, today_man, today_woman, today_sex_null ]
        tmp_se = pd.Series(p_array, index=df_patients.columns)
        df_patients = df_patients.append(tmp_se, ignore_index = True)
        print(p_array)

        goukei_age = today_20 + today_40 + today_60 + today_80 + today_100 + today_age_null
        print("年齢別の人数の合計＝" + str(goukei_age) )
        goukei_sex = today_man + today_woman + today_sex_null
        print("性別の人数の合計＝" + str(goukei_sex) )

        df_patients.to_csv(covid19_path + "\\自動作成ファイル\\patients_age_sex.csv", index=None, encoding='CP932')
else:
    print("必要なファイルがない")


