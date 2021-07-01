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

if(os.path.exists(CSV_path + "\\hakodate_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】

    #pandasでCSVファイルを読み込み
    csv_read_df = pd.read_csv(CSV_path + "\\hakodate_" + dt_mmdd + ".csv",encoding="CP932")

    #データフレームを作成（カラムのみ指定） 参考ページ【https://qiita.com/567000/items/d8a29bb7404f68d90dd4】
    csv_df = pd.DataFrame( columns=["例目","年代","性別","居住地","職業","現状","補足","再陽性FG","発症日","発症年月日","症状元","患者_症状","渡航FG","備考","エラー"])

    #行の検査用
    ken_num = 0
    df_FLG = False
    no_kokuseki = 0
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_read_df)):
        if df_FLG and str(csv_read_df.iloc[i,0])!="nan": #フラグが立っている間の処理
            if "施設等名称" in str(csv_read_df.iloc[i,0]):
                break
            
            if "例目" in str(csv_read_df.iloc[i,1]): #「例目」以外なら処理
                p_error = ""
            else:
                p_num = int((csv_read_df.iloc[i,col_num]).replace(",",""))  #例目
                p_residence = str(csv_read_df.iloc[i,col_residence])  #居住地

                p_error = ""
                #居住地を振興局に変換
                if "渡島" in p_residence or "函館市" in p_residence:
                    p_residence = "渡島総合振興局管内"
                elif "非公表" in p_residence:
                    p_residence = "非公表"
                else:
                    p_residence = p_residence.replace
                    p_error = "振興局該当なし："

                p_sex = str(csv_read_df.iloc[i,col_sex])  #性別
                p_age = str(csv_read_df.iloc[i,col_age])  #年齢
                
                if "未満" in p_age : #10歳未満か判別
                    p_age = "10歳未満"
                else:
                    p_age = p_age.replace("歳","")
                if "代" in p_age:
                    p_age = p_age
                else:
                    if p_age == "非公表":
                        p_age = p_age
                    elif p_age == "10歳未満":
                        p_age = p_age
                    else:
                        p_age = p_age + "代"

                p_status = str(csv_read_df.iloc[i,col_status])  #現状
                
                p_error = ""
                
                #配列にして、データフレームに追加
                #["例目","年代","性別","居住地","職業","現状","補足","再陽性FG","発症日","発症年月日","症状元","患者_症状","渡航FG","備考","エラー"])
                tmp_se = pd.Series([ p_num, p_age, p_sex, p_residence, "", p_status, "", "", "", "", "", "", "0", "", "" ], index=csv_df.columns)
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
        if "No" in str(csv_read_df.iloc[i,0]) :
            #「No」の次の行からフラグをたてる
            df_FLG = True
            #データのある列番号を更新
            for j in range(len(csv_read_df.columns)):
                if "例目" in str(csv_read_df.iloc[i,j]):
                    col_num = j+1
                if "居住地" in str(csv_read_df.iloc[i,j]):
                    col_residence = j+1 
                if "性別" in str(csv_read_df.iloc[i,j]):
                    col_sex = j+1
                if "年代" in str(csv_read_df.iloc[i,j]):
                    col_age = j+1
                if "現在の" in str(csv_read_df.iloc[i,j]):
                    col_status = j+1
            
        # elif str(csv_read_df.iloc[i+1,0]) == "nan" and str(csv_read_df.iloc[i+1,1]) == "nan" and str(csv_read_df.iloc[i+1,2]) == "nan":
        #     #1列目(A)、2列名(B)、3列名(C)が空白の場合はフラグを終了
        #     df_FLG = False
            
    print(csv_df) 
    csv_df.to_csv(CSV_path + "\\list_hakodate_" + dt_mmdd + ".csv", index=None, encoding='CP932')
else:
    print("函館の患者一覧無し") 