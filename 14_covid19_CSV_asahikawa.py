import os
import pandas as pd
import file_day
import pdf_download_path
from datetime import datetime, date, timedelta
#数値入力用のシンプルダイアログの表示
import tkinter as tk
import tkinter.simpledialog as simpleDialog

#【2021/01/19 一覧形式に変更された】
print("＝＝＝＝14_covid19_CSV_asahikawa.py＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝")
#今日の日付
today = datetime.today()
dt_mmdd = file_day.f_today()
print("今日は" + dt_mmdd)

#CSVのフォルダを指定
CSV_path = pdf_download_path.p_path()

if(os.path.exists(CSV_path + "\\asahikawa_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】

    #pandasでCSVファイルを読み込み
    csv_old_df = pd.read_csv(CSV_path + "\\asahikawa_" + dt_mmdd + ".csv",encoding="CP932")
    print("\\asahikawa_" + dt_mmdd + ".csv を処理中")

    #必要な変数を設定
    myFLG = False

    d_kamikawa = 0
    d_sonota = 0
    d_asahikawa_igai = 0
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
    d_sex_hikouhyou = 0
    d_mushoujyou = 0
    d_keishou = 0
    d_tyoutoushou = 0
    d_jyoushou = 0
    d_genjyou_fumei = 0

    #=======振興局ごとの人数=======
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_old_df)-1):
        #数値が２列目にある前提
        if "旭川市" == str(csv_old_df.iloc[i,0]):
            new_text = str(csv_old_df.iloc[i,1]).replace(".0","") 
            d_kamikawa = int(new_text)  #旭川市の人数
        if "旭川市外(道内)" == str(csv_old_df.iloc[i,0]):
            new_text = str(csv_old_df.iloc[i,1]).replace(".0","") #「)」を削除
            d_asahikawa_igai  = int(new_text)  #旭川市外の人数
        if "旭川市外(道外)" == str(csv_old_df.iloc[i,0]):
            new_text = str(csv_old_df.iloc[i,1]).replace(".0","") #「)」を削除
            d_sonota  = int(new_text)  #旭川市外の人数

    day_total_shinkoukyoku = d_kamikawa + d_sonota + d_asahikawa_igai
    day_total = day_total_shinkoukyoku
    #振興局別の患者数CSVを作成
    csv_shinkoukyoku_df = pd.DataFrame()
    read_se = pd.Series(["集計","地域","空知","石狩","後志","胆振","日高","渡島","檜山","上川","留萌","宗谷","オホーツク","十勝","釧路","根室","道外他","非公表","重複削除","日計"])
    csv_shinkoukyoku_df = csv_shinkoukyoku_df.append(read_se, ignore_index = True)
    tmp_se = pd.Series(["集計","旭川市", 0,0,0,0,0,0,0,d_kamikawa,0,0,0,0,0,0,d_sonota,d_asahikawa_igai,0,day_total ], index=csv_shinkoukyoku_df.columns)
    csv_shinkoukyoku_df = csv_shinkoukyoku_df.append(tmp_se, ignore_index = True)
    print(csv_shinkoukyoku_df) 
    csv_shinkoukyoku_df.to_csv(CSV_path + "\\day_asahikawa_shinkoukyoku_" + dt_mmdd + ".csv",index=None,header=False, encoding="CP932")
    #print(day_total_shinkoukyoku)

    #=======年代ごとの人数=======
    if day_total_shinkoukyoku != 0:
        for i in range(len(csv_old_df)-1):
            #１列目にある前提
            if "10歳未満" in str(csv_old_df.iloc[i,0]):
                d_age01 = int(str(csv_old_df.iloc[i,1]).replace(".0",""))  
                d_age10 = int(str(csv_old_df.iloc[i+1,1]).replace(".0",""))  
                d_age20 = int(str(csv_old_df.iloc[i+2,1]).replace(".0",""))  
                d_age30 = int(str(csv_old_df.iloc[i+3,1]).replace(".0",""))  
                d_age40 = int(str(csv_old_df.iloc[i+4,1]).replace(".0","")) 
                d_age50 = int(str(csv_old_df.iloc[i+5,1]).replace(".0","")) 
                d_age60 = int(str(csv_old_df.iloc[i+6,1]).replace(".0",""))  
                d_age70 = int(str(csv_old_df.iloc[i+7,1]).replace(".0",""))  
                d_age80 = int(str(csv_old_df.iloc[i+8,1]).replace(".0",""))  
                d_age90 = int(str(csv_old_df.iloc[i+9,1]).replace(".0",""))  
                d_age_hikouhyou = int(str(csv_old_df.iloc[i+10,1]).replace(".0",""))  
                break

    day_total = d_age01+d_age10+d_age20+d_age30+d_age40+d_age50+d_age60+d_age70+d_age80+d_age90+d_age_hikouhyou
    #年代別の患者数CSVを作成
    csv_age_df = pd.DataFrame()
    read_se = pd.Series(["集計","地域","10歳未満","10歳代","20歳代","30歳代","40歳代","50歳代","60歳代","70歳代","80歳代","90歳代以上","非公表","重複削除","日計"])
    csv_age_df = csv_age_df.append(read_se, ignore_index = True)
    tmp_se = pd.Series(["集計","旭川市", d_age01,d_age10,d_age20,d_age30,d_age40,d_age50,d_age60,d_age70,d_age80,d_age90,d_age_hikouhyou,0,day_total ], index=csv_age_df.columns)
    csv_age_df = csv_age_df.append(tmp_se, ignore_index = True)
    print(csv_age_df) 
    csv_age_df.to_csv(CSV_path + "\\day_asahikawa_age_" + dt_mmdd + ".csv",index=None,header=False, encoding="CP932")

    #=======状態ごとの人数=======
    if day_total_shinkoukyoku != 0:
        for i in range(len(csv_old_df)-1):
            for j in range(len(csv_old_df.columns)):
                #３列目にある前提
                if "無症状" in str(csv_old_df.iloc[i,j]) and "軽症" in str(csv_old_df.iloc[i+1,j]): #データが複数のセルに分かれている場合
                    d_mushoujyou = int(str(csv_old_df.iloc[i,j+1]).replace(".0",""))
                    d_keishou = int(str(csv_old_df.iloc[i+1,j+1]).replace(".0",""))
                    d_tyoutoushou = int(str(csv_old_df.iloc[i+2,j+1]).replace(".0",""))
                    d_jyoushou = int(str(csv_old_df.iloc[i+3,j+1]).replace(".0",""))
                    d_genjyou_fumei = int(str(csv_old_df.iloc[i+4,j+1]).replace(".0",""))
                    break


    day_total = d_mushoujyou+d_keishou+d_tyoutoushou+d_jyoushou+d_genjyou_fumei
    #状態別の患者数CSVを作成
    csv_status_df = pd.DataFrame()
    read_se = pd.Series(["集計","地域","無症状","軽症","中等症","重症","非公表","重複削除","日計"])
    csv_status_df = csv_status_df.append(read_se, ignore_index = True)
    tmp_se = pd.Series(["集計","旭川市", d_mushoujyou,d_keishou,d_tyoutoushou,d_jyoushou,d_genjyou_fumei,0,day_total ], index=csv_status_df.columns)
    csv_status_df = csv_status_df.append(tmp_se, ignore_index = True)
    print(csv_status_df) 
    csv_status_df.to_csv(CSV_path + "\\day_asahikawa_status_" + dt_mmdd + ".csv",index=None,header=False, encoding="CP932")

    #=======性別ごとの人数=======
    if day_total_shinkoukyoku != 0:
        for i in range(len(csv_old_df)-1):
            for j in range(len(csv_old_df.columns)):
                #合計が隣の列にある前提
                if "男性" in str(csv_old_df.iloc[i,j]):
                    sex_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                    d_man = int(sex_arr[0].replace(".0",""))
                if "女性" in str(csv_old_df.iloc[i,j]):
                    sex_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                    d_woman = int(sex_arr[0].replace(".0",""))
                if "調査中" in str(csv_old_df.iloc[i,j]) and "女性" in str(csv_old_df.iloc[i-1,j]):
                    sex_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                    d_sex_hikouhyou = int(sex_arr[0].replace(".0",""))
                    break
            if "女性" in str(csv_old_df.iloc[i,j]):
                break

    day_total = d_man + d_woman + d_sex_hikouhyou
    #性別別の患者数CSVを作成
    csv_sex_df = pd.DataFrame()
    read_se = pd.Series(["集計","地域","男性","女性","非公表","重複削除","日計"])
    csv_sex_df = csv_sex_df.append(read_se, ignore_index = True)
    tmp_se = pd.Series(["集計","旭川市", d_man,d_woman,d_sex_hikouhyou,0,day_total ], index=csv_sex_df.columns)
    csv_sex_df = csv_sex_df.append(tmp_se, ignore_index = True)
    print(csv_sex_df) 
    csv_sex_df.to_csv(CSV_path + "\\day_asahikawa_sex_" + dt_mmdd + ".csv",index=None,header=False, encoding="CP932")
else:
    print("旭川市の患者一覧無し") 