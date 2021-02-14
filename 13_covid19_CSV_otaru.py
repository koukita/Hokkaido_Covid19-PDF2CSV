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

if(os.path.exists(CSV_path + "\\otaru_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    #pandasでCSVファイルを読み込み
    csv_read_df = pd.read_csv(CSV_path + "\\otaru_" + dt_mmdd + ".csv",encoding="CP932")
    #データフレームを作成（カラムのみ指定） 参考ページ【https://qiita.com/567000/items/d8a29bb7404f68d90dd4】
    csv_df = pd.DataFrame( columns=["例目","年代","性別","居住地","職業","現状","補足","再陽性FG","発症日","発症年月日","症状元","患者_症状","渡航FG","備考","エラー"])

    #行の検査用
    ken_num = 0
    df_FLG = False
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_read_df)-1):
        if df_FLG: #フラグが立っている間の処理
            p_num = str(csv_read_df.iloc[i,2])  #例目
            p_residence = str(csv_read_df.iloc[i,3])  #居住地
            #居住地を振興局に変換
            if p_residence == "小樽市":
                p_residence = "後志総合振興局管内"
                p_error = ""
            elif p_residence == "非公表":
                p_residence = "非公表"
                p_error = ""
            else:
                p_residence = p_residence
                p_error = "振興局該当なし："

            p_sex = str(csv_read_df.iloc[i,5])  #性別
            p_age = str(csv_read_df.iloc[i,6])  #年齢
            if "未満" in p_age : #10歳未満か判別
                p_age = "10歳未満"
            else:
                p_age = p_age.replace("歳","")
            p_job = str(csv_read_df.iloc[i,7])  #職業
            p_status = str(csv_read_df.iloc[i,8])  #現状
            c_hassho = str(csv_read_df.iloc[i,9]).replace(" ","")  #発症日 ※半角スペースを除く
            if "月" in c_hassho and "日" in c_hassho:
                c_year = int(datetime.strftime(today,'%Y')) #int関数で数値に変換
                c_month = int(c_hassho[0:c_hassho.find("月")])
                c_day = int(c_hassho[c_hassho.find("月")+1:c_hassho.find("日")])
                p_Hday = "{year}-{month:02}-{day:02}".format(year=c_year,month=c_month,day=c_day)
                p_bikou = ""
            elif "非公表" in c_hassho:
                p_Hday = ""
                p_bikou = "発症日は非公表"
            elif "無症状" in c_hassho:
                p_Hday = ""
                p_bikou = ""
            else:
                p_Hday = ""
                p_bikou = ""
            p_symptons = "非公表" #症状
            p_error = ""
            
            #配列にして、データフレームに追加
            #["例目","年代","性別","居住地","職業","現状","補足","再陽性FG","発症日","発症年月日","症状元","患者_症状","渡航FG","備考","エラー"])
            tmp_se = pd.Series([ p_num, p_age, p_sex, p_residence, p_job, p_status, "", "", "", p_Hday, "", p_symptons, "0", p_bikou, p_error ], index=csv_df.columns)
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
        if str(csv_read_df.iloc[i-1,0]) == "No": #1行前
            #「No」の次の行からフラグをたてる
            df_FLG = True
        elif str(csv_read_df.iloc[i+1,10]) == "nan": #1行先
            #11列目が空白の場合はフラグを終了
            df_FLG = False

    print(csv_df) 
    csv_df.to_csv(CSV_path + "\\list_otaru_" + dt_mmdd + ".csv", index=None, encoding="CP932")
else:
    print("小樽の患者一覧無し") 