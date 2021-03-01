import os
import csv
import pandas as pd
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
if(os.path.exists(covid19_path + "\\covid19_data.csv")) and (os.path.exists(download_path + "\\ruikei_" + dt_mmdd_today + ".csv")):
    #pandasでCSVファイルを読み込み
    df_covid19 = pd.read_csv(covid19_path + "\\covid19_data.csv", encoding="CP932", 
                dtype={"日検査数": int, "検査累計": int, "日陽性数": int, "陽性累計": int, "日患者数": int, "患者累計": int, "日軽症中等症数": int
                , "軽症中等症累計": int, "日重症数": int, "重症累計": int, "日死亡数": int, "死亡累計": int, "日治療終了数": int
                , "治療終了累計": int, "新規検査人数計": int, "濃厚接触者": int, "濃厚接触者以外": int, "ステージ": int})
    df_ruikei = pd.read_csv(download_path + "\\ruikei_" + dt_mmdd_today + ".csv", encoding="CP932")

    #前日までの合計を取得
    mae_year = int(df_covid19.iloc[len(df_covid19)-1,1])
    mae_month = int(df_covid19.iloc[len(df_covid19)-1,2])
    mae_day = int(df_covid19.iloc[len(df_covid19)-1,3])
    mae_kensa_rui = int(df_covid19.iloc[len(df_covid19)-1,5])
    mae_yousei_rui = int(df_covid19.iloc[len(df_covid19)-1,7])
    mae_kanjya_rui = int(df_covid19.iloc[len(df_covid19)-1,9])
    mae_keishou_rui = int(df_covid19.iloc[len(df_covid19)-1,11])
    mae_jyushou_rui = int(df_covid19.iloc[len(df_covid19)-1,13])
    mae_sibou_rui = int(df_covid19.iloc[len(df_covid19)-1,15])
    mae_insei_rui = int(df_covid19.iloc[len(df_covid19)-1,17])

    #今日のデータを取得
    today_kensa_rui = int(df_ruikei.iloc[0,0])
    today_yousei_rui = int(df_ruikei.iloc[0,1])
    today_kanjya_rui = int(df_ruikei.iloc[0,2])
    today_keishou_rui = int(df_ruikei.iloc[0,3])
    today_jyushou_rui = int(df_ruikei.iloc[0,4])
    today_sibou_rui = int(df_ruikei.iloc[0,5])
    today_insei_rui = int(df_ruikei.iloc[0,6])
    today_sinkensa = int(df_ruikei.iloc[0,7])
    today_noukou = int(df_ruikei.iloc[0,8])
    today_noukouigai = int(df_ruikei.iloc[0,9])

     #今日の日付
    if d_year == mae_year and d_month == mae_month and today == mae_day:
        print("すでに今日のデータがあります。プログラムを終了します。")
    else:
        #ファイルをバックアップする
        shutil.copyfile(covid19_path + "\\covid19_data.csv", covid19_path + "\\backup\\covid19_data_backup" + dt_mmdd_today + ".csv")

        #今日のデータを追加
        today_kensa = int(today_kensa_rui - mae_kensa_rui)
        today_yousei = int(today_yousei_rui - mae_yousei_rui)
        today_kanjya = int(today_kanjya_rui - mae_kanjya_rui) 
        today_keishou = int(today_keishou_rui - mae_keishou_rui)
        today_jyushou = int(today_jyushou_rui - mae_jyushou_rui)
        today_sibou = int(today_sibou_rui - mae_sibou_rui)
        today_insei = int(today_insei_rui - mae_insei_rui)
        today_youseiritu = Decimal(str((today_yousei / today_sinkensa)*100)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        
        #配列を作る
        p_array =["", d_year, d_month, today, today_kensa, today_kensa_rui, today_yousei, today_yousei_rui,
                today_kanjya, today_kanjya_rui, today_keishou, today_keishou_rui, today_jyushou, today_jyushou_rui, 
                today_sibou, today_sibou_rui, today_insei, today_insei_rui, today_sinkensa, today_youseiritu, 
                today_noukou, today_noukouigai,"",3]
        tmp_se = pd.Series(p_array, index=df_covid19.columns)
        df_covid19 = df_covid19.append(tmp_se, ignore_index = True)
        print(p_array)


        df_covid19.to_csv(covid19_path + "\\自動作成ファイル\\covid19_data.csv", index=None, encoding='CP932')
else:
    print("必要なファイルがない")


