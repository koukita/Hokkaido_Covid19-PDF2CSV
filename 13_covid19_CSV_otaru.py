import os
from numpy import False_, floor
import pandas as pd
import file_day
import pdf_download_path
from datetime import datetime, date, timedelta

print("＝＝＝＝13_covid19_CSV_otaru.py＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝")
#今日の日付
today = datetime.today()
dt_mmdd = file_day.f_today()
print("今日は" + dt_mmdd)

#CSVのフォルダを指定
CSV_path = pdf_download_path.p_path()

#累計用の配列を用意
ruikei_arr =[]

if(os.path.exists(CSV_path + "\\otaru_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    #pandasでCSVファイルを読み込み
    csv_old_df = pd.read_csv(CSV_path + "\\otaru_" + dt_mmdd + ".csv",encoding="CP932")
    print("\\otaru_" + dt_mmdd + ".csv を処理中")
    #1つの列に2つのデータが有る場合があるので、CSVを修正したデータフレームを作成
    myFLG = False

    d_shiribeshi = 0
    d_shinkoukyoku_hikouhyou = 0
    d_age01 = 0
    d_age10 = 0
    d_age20 = 0
    d_age30 = 0
    d_age40 = 0
    d_age50 = 0
    d_age60 = 0
    d_age70 = 0
    d_age80 = 0
    d_age90 = 0
    d_age100 = 0
    d_age_hikouhyou = 0
    d_man = 0
    d_woman = 0
    d_mushoujyou = 0
    d_keishou = 0
    d_tyoutoushou = 0
    d_jyoushou = 0

    #=======小樽のデータを作成=======
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_old_df)-1):
        #合計が３列目にある前提
        if "小樽" in str(csv_old_df.iloc[i,0]):
            d_shiribeshi = int(csv_old_df.iloc[i+1,0])
            d_shinkoukyoku_hikouhyou = int(csv_old_df.iloc[i+1,1])
            d_man = int(csv_old_df.iloc[i+1,2])
            d_woman = int(csv_old_df.iloc[i+1,3])
            d_mushoujyou = int(csv_old_df.iloc[i+1,4])
            d_keishou = int(csv_old_df.iloc[i+1,5])
            d_tyoutoushou = int(csv_old_df.iloc[i+1,6])
            d_jyoushou = int(csv_old_df.iloc[i+1,7])
            d_age_hikouhyou = d_shiribeshi + d_shinkoukyoku_hikouhyou

    #CSVを作成
    csv_df = pd.DataFrame()
    read_se = pd.Series(["小樽","振興局非公表","男性","女性","無症状","軽症","中等症","重症","年代非公表"])
    csv_df = csv_df.append(read_se, ignore_index = True)
    tmp_se = pd.Series([d_shiribeshi,d_shinkoukyoku_hikouhyou, d_man,d_woman,d_mushoujyou,d_keishou,d_tyoutoushou,d_jyoushou,d_age_hikouhyou ], index=csv_df.columns)
    csv_df = csv_df.append(tmp_se, ignore_index = True)
    #print(csv_df) 
    csv_df.to_csv(CSV_path + "\\day_otaru_" + dt_mmdd + ".csv",index=None,header=False, encoding="CP932")



else:
    print("小樽まとめの患者一覧無し") 