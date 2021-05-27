import os
import pandas as pd
import file_day
import pdf_download_path
from datetime import datetime, date, timedelta

#今日の日付   
today = datetime.today()
dt_mmdd = file_day.f_today()
print("今日は" + dt_mmdd)

#CSVのフォルダを指定
CSV_path = pdf_download_path.p_path()

if(os.path.exists(CSV_path + "\\asahikawa_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    #pandasでCSVファイルを読み込み
    csv_read_df = pd.read_csv(CSV_path + "\\asahikawa_" + dt_mmdd + ".csv",encoding="CP932")
    #データフレームを作成（カラムのみ指定） 参考ページ【https://qiita.com/567000/items/d8a29bb7404f68d90dd4】
    csv_df = pd.DataFrame( columns=["例目","年代","性別","居住地","職業","現状","補足","再陽性FG","発症日","発症年月日","症状元","患者_症状","渡航FG","備考","エラー"])

    #行の検査用
    ken_num = 0
    df_FLG = False
    ck_num = 0
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_read_df)):
        if df_FLG: #フラグが立っている間の処理
            #print(str(csv_read_df.iloc[i,0]))
            if str(csv_read_df.iloc[i,0]) == "nan": #1列目が空白なら、列がずれているので1列ずらす
                c_col = 1
            else:
                c_col = 0           
            p_num = str(csv_read_df.iloc[i,c_col + 2])  #例目
            p_residence = str(csv_read_df.iloc[i,c_col + 4])  #居住地
            #居住地を振興局に変換
            if p_residence == "旭川市":
                p_residence = "上川総合振興局管内"
                p_error = ""
            elif p_residence == "非公表":
                p_residence = "非公表"
                p_error = ""
            else:
                p_residence = p_residence
                p_error = "振興局該当なし："

            p_sex = str(csv_read_df.iloc[i,c_col + 6])  #性別
            p_age = str(csv_read_df.iloc[i,c_col + 5])  #年齢
            if "未満" in p_age : #10歳未満か判別
                p_age = "10歳未満"
            else:
                p_age = p_age.replace("歳","")
            p_job = str(csv_read_df.iloc[i,c_col + 7])  #職業
            p_status = "非公表"  #現状
            p_Hday = "" #発症日
            p_symptons = "非公表" #症状
            p_error = ""
            p_bikou = "発症日は非公表"
            
            if str(csv_read_df.iloc[i,0]) == "nan" or p_num == "nan" or p_residence == "nan":
                p_num = ""
            else:
                #配列にして、データフレームに追加
                #["例目","年代","性別","居住地","職業","現状","補足","再陽性FG","発症日","発症年月日","症状元","患者_症状","渡航FG","備考","エラー"])
                tmp_se = pd.Series([ p_num, p_age, p_sex, p_residence, p_job, p_status, "", "0", "", p_Hday, "", p_symptons, "0", p_bikou, p_error ], index=csv_df.columns)
                csv_df = csv_df.append(tmp_se, ignore_index = True)

            p_num = ""
            p_residence = ""
            p_sex = ""
            p_age = ""
            p_job = ""
            p_status = ""
            p_Hday = ""
            p_bikou = ""
            p_symptons = ""
            p_error = ""

        #データフレームに入力する行かの判断
        if str(csv_read_df.iloc[i,1]) == "市内番号":
            df_FLG = True
        #     if str(csv_read_df.iloc[i+1,0]) == "nan": #次の行の1列目が空白なら、列がずれているので1列ずらす
        #         c_col = 1
        #     else:
        #         c_col = 0
            
        #     if str(csv_read_df.iloc[i+1,c_col+2]) == ck_num: #すでに登録された番号か確認
        #         df_FLG = False
        #     else:
        #         df_FLG = True
        #         ck_num = str(csv_read_df.iloc[i+1,c_col+2])
        # elif str(csv_read_df.iloc[i,2]) == "nan":
        #     if str(csv_read_df.iloc[i+1,2]) == "nan":
        #         #その行の2列目が空白で、次の行も空白の場合はフラグを終了
        #         df_FLG = False

    #print(csv_df) 
    csv_df.to_csv(CSV_path + "\\list_asahikawa_" + dt_mmdd + ".csv", index=None, encoding="CP932")
else:
    print("旭川の患者一覧無し") 