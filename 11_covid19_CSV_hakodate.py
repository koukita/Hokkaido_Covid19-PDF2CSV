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
    p_error = ""
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_read_df)):
        for j in range(len(csv_read_df.columns)): #1列目から順番に読み込み
            c_txt = str(csv_read_df.iloc[i,j]).replace(" ","") #半角スペースを除去
            c_txtArr = c_txt.splitlines()
            if "例目)" in c_txt:
                #道内番号
                p_num = c_txtArr[1].replace("(道内","").replace("例目)","")
                p_num = int(p_num.replace(",",""))
                if ken_num != 0: #1ブロック目ではない
                    if (i - ken_num) != 8: #ブロック間隔が9行ではない場合
                        p_error = "1つ前との行間NG"
                    else:
                        p_error = "OK"
                else:
                    p_error = "OK1"

                ken_num = i
                #居住地
                p_residence = c_txtArr[5].replace("居住地:","")
                #居住地を振興局に変換
                if p_residence == "函館市":
                    p_residence = "渡島総合振興局管内"
                    p_error =  p_error + ""
                elif p_residence == "非公表":
                    p_residence = "非公表"
                    p_error =  p_error + ""
                else:
                    p_residence = p_residence
                    p_error =  p_error + ",振興局該当なし："
                #性別
                p_sex = c_txtArr[3].replace("性別:","")
                #年齢
                p_age = c_txtArr[2].replace("年代:","")
                if "未満" in p_age: #10歳未満か判別
                    p_age = "10歳未満"
                else:
                    p_age = p_age.replace("歳","")
                #職業
                p_job = c_txtArr[6].replace("職業:","")
            elif "現在の状況" in c_txt:
                c_txt = str(csv_read_df.iloc[i,j+1]) #一つ右のセルの値を取得
                if "非公表" in c_txt:
                    p_status = "非公表"
                else:
                    p_status = c_txt[c_txt.rfind(" ")+1:len(c_txt)] #後ろから文字を検索
            elif "発症日" in c_txt:
                c_txt = str(csv_read_df.iloc[i,j+1]) #一つ右のセルの値を取得
                if "月" in c_txt:
                    c_year = int(datetime.strftime(today,'%Y')) #int関数で数値に変換
                    c_month = int(c_txt[0:c_txt.find("月")])
                    c_day = int(c_txt[c_txt.find("月")+1:len(c_txt)-1])
                    p_Hday = "{year}-{month:02}-{day:02}".format(year=c_year,month=c_month,day=c_day)
                    p_bikou = ""
                elif "非公表" in c_txt:
                    p_Hday = ""
                    p_bikou = "発症日は非公表"
                elif "-" in c_txt:
                    p_Hday = ""
                    p_bikou = ""
            elif "主な症状" in c_txt:
                c_txt = str(csv_read_df.iloc[i,j+1]) #一つ右のセルの値を取得
                if "無症状" in c_txt:
                    p_symptons = "症状なし"
                elif "非公表" in c_txt:
                    p_symptons = "非公表"
                else:
                    p_symptons = c_txt.replace("主な症状 ","").replace(",",";")

            elif "行動歴" in c_txt:
                #ブロック最後の行なので書き込み用データフレームに1行を追加
                # ["例目","年代","性別","居住地","職業","現状","補足","再陽性FG","発症日","発症年月日","症状元","患者_症状","渡航FG","備考","エラー"]
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
            
    print(csv_df) 
    csv_df.to_csv(CSV_path + "\\list_hakodate_" + dt_mmdd + ".csv", index=None, encoding="CP932")
else:
    print("函館の患者一覧無し") 