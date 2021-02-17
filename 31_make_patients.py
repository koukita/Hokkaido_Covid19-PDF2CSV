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
if(os.path.exists(covid19_path + "\\patients.csv")) and (os.path.exists(download_path + "\\hasseijyoukyouitiran" + dt_mmdd_yday + ".csv")) and (os.path.exists(download_path + "\\csv_merge_" + dt_mmdd_today + ".csv")):
    #pandasでCSVファイルを読み込み
    df_patients = pd.read_csv(covid19_path + "\\patients.csv", encoding="CP932")
    df_csv_merge = pd.read_csv(download_path + "\\csv_merge_" + dt_mmdd_today + ".csv", encoding="CP932")
    df_csv_hassei = pd.read_csv(download_path + "\\hasseijyoukyouitiran" + dt_mmdd_yday + ".csv", encoding="CP932")
    #print(df_patients.loc[11].values)
    #更新用のデータフレームを作成 ※既存のpatients.csvから現在のNoから11000行目のみ取り出したのも
    df_e_pati = df_patients.iloc[0:10000+ len(df_csv_hassei)-1000,:]
    #print(df_e_pati)
    
    #一番最後の行を確認し、今日の日付なら終了
    last_day = str(df_patients.iloc[len(df_patients)-1,1])
    #今日の日付
    today_day = file_day.long_txt_day()
    if today_day == last_day:
        print("すでに今日のデータがあります。プログラムを終了します。")
        sys.exit()

    #ファイルをバックアップする
    shutil.copyfile(covid19_path + "\\patients.csv", covid19_path + "\\backup\\patients_backup" + dt_mmdd_today + ".csv")

    #公表患者情報を1行ずつ確認し、同じ番号のデータを取得
    for gyou_hassei in range(len(df_csv_hassei)-1000,len(df_csv_hassei)):
        p_No = str(df_csv_hassei.iloc[gyou_hassei,0]) #No
        p_hassei = str(df_csv_hassei.iloc[gyou_hassei,5]) #発生
        p_jyoukyou = str(df_csv_hassei.iloc[gyou_hassei,6]) #状況
        #print(p_No)
        # #既存の「patients.csv」データフレームを2000行前から読み込む
        for gyou_patients in range(len(df_patients)-2000-1,len(df_patients)):
            if p_No == str(df_patients.iloc[gyou_patients,0]):
                #print("pati" + str(df_patients.iloc[gyou_patients,0]))
                p_day = str(df_patients.iloc[gyou_patients,1]) #リリース日
                p_kyojyu = str(df_patients.iloc[gyou_patients,3]) #居住地
                p_age = str(df_patients.iloc[gyou_patients,4]) #年代
                p_sex = str(df_patients.iloc[gyou_patients,5]) #性別
                p_zokusei = str(df_patients.iloc[gyou_patients,6]) #属性（職業）
                p_bikou = str(df_patients.iloc[gyou_patients,7]) #備考
                p_age_group = str(df_patients.iloc[gyou_patients,12]) #年齢のグループ
                p_sex_en = str(df_patients.iloc[gyou_patients,13]) #英語性別

                #配列を作る
                p_array = [p_No, p_day, "", p_kyojyu, p_age, p_sex, p_zokusei, p_bikou, "", "", p_hassei, p_jyoukyou, p_age_group, p_sex_en ]
                #リストを検索し、「nan」を空白に置き換え
                for index,value in enumerate(p_array):
                    if value == "nan":
                        p_array[index] = ""

                tmp_se = pd.Series(p_array, index=df_e_pati.columns)
                df_e_pati = df_e_pati.append(tmp_se, ignore_index = True)
                print(p_array)
    
    #今日のデータを追加
    for gyou_today in range(0,len(df_csv_merge)):
        p_No = str(df_csv_merge.iloc[gyou_today,0]) #No
        p_day = file_day.long_txt_day() #リリース日
        p_kyojyu = str(df_csv_merge.iloc[gyou_today,3]) #居住地
        p_age = str(df_csv_merge.iloc[gyou_today,1]) #年代
        p_sex = str(df_csv_merge.iloc[gyou_today,2]) #性別
        p_zokusei = str(df_csv_merge.iloc[gyou_today,4]) #属性（職業）
        p_bikou = str(df_csv_merge.iloc[gyou_today,5]) #備考（現状）
        #年齢のグループ
        if p_age == "10歳未満" or p_age == "10代":
            p_age_group = 10
        elif p_age == "20代":
            p_age_group = 20
        elif p_age == "30代":
            p_age_group = 30
        elif p_age == "40代":
            p_age_group = 40
        elif p_age == "50代":
            p_age_group = 50
        elif p_age == "60代":
            p_age_group = 60
        elif p_age == "70代":
            p_age_group = 70
        elif p_age == "80代":
            p_age_group = 80
        elif p_age == "90代":
            p_age_group = 90
        elif p_age == "100代":
            p_age_group = 100
        else:
            p_age_group = 0
        
        #英語性別
        if p_sex == "男性":
            p_sex_en = "man"
        elif p_sex == "女性":
            p_sex_en = "woman"
        else:
            p_sex_en = "-"
        #配列を作る
        p_array =[p_No, p_day, "", p_kyojyu, p_age, p_sex, p_zokusei, p_bikou, "", "", "", "", p_age_group, p_sex_en ]
        #リストを検索し、「nan」を空白に置き換え
        for index,value in enumerate(p_array):
            if value == "nan":
                p_array[index] = ""

        tmp_se = pd.Series(p_array, index=df_e_pati.columns)
        df_e_pati = df_e_pati.append(tmp_se, ignore_index = True)
        print(p_array)

    df_e_pati.to_csv(covid19_path + "\\自動作成ファイル\\patients.csv", index=None, encoding='CP932')
else:
    print("必要なファイルがない")


