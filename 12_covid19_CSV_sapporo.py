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

if(os.path.exists(CSV_path + "\\sapporo_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】

    #pandasでCSVファイルを読み込み
    csv_read_df = pd.read_csv(CSV_path + "\\sapporo_" + dt_mmdd + ".csv",encoding="CP932")

    #データフレームを作成（カラムのみ指定） 参考ページ【https://qiita.com/567000/items/d8a29bb7404f68d90dd4】
    csv_df = pd.DataFrame( columns=["例目","年代","性別","居住地","職業","現状","補足","再陽性FG","発症日","発症年月日","症状元","患者_症状","渡航FG","備考","エラー"])

    #行の検査用
    ken_num = 0

    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_read_df)-1):
        for j in range(len(csv_read_df.columns)-1): #1列目から順番に読み込み
            c_txt = str(csv_read_df.iloc[i,j]) #値を文字列に変換して記録
            if "道内" in c_txt:
                p_num = int(c_txt.replace("道内","").replace("例目",""))
                p_error = "OK1"
                if ken_num != 0: #1ブロック目ではない
                    if (i - ken_num) != 9: #ブロック間隔が9行ではない場合
                        p_error = "1つ前との行間NG"
                    else:
                        p_error = "OK"
                ken_num = i
            elif "居住地" in c_txt:
                p_residence = c_txt.replace("居住地: ","")
                #居住地を振興局に変換
                if p_residence == "札幌市":
                    p_residence = "石狩振興局管内"
                    p_error = p_error + ""
                elif p_residence == "非公表":
                    p_residence = "非公表"
                    p_error = p_error + ""
                else:
                    p_residence = p_residence
                    p_error =  p_error + ",振興局該当なし："

            elif "性別" in c_txt:
                p_sex = c_txt.replace("性別: ","")
            elif "年代" in c_txt:
                if "未満" in c_txt: #10歳未満か判別
                    p_age = "10歳未満"
                else:
                    p_age = c_txt.replace("年代: ","").replace("歳","")
            elif "職業" in c_txt:
                p_job = c_txt.replace("職業: ","")
            elif "現状" in c_txt:
                if "非公表" in c_txt:
                    p_status = "非公表"
                else:
                    p_status = csv_read_df.iloc[i+1,j].replace("・","")
            elif "発症日" in c_txt:
                if "月" in c_txt:
                    c_year = int(datetime.strftime(today,'%Y')) #int関数で数値に変換
                    c_month = int(c_txt[5:c_txt.find("月")])
                    c_day = int(c_txt[c_txt.find("月")+1:c_txt.find("日(")])
                    p_Hday = "{year}-{month:02}-{day:02}".format(year=c_year,month=c_month,day=c_day)
                    p_bikou = ""
                elif "非公表" in c_txt:
                    p_Hday = ""
                    p_bikou = "発症日は非公表"
                elif "-" in c_txt:
                    p_Hday = ""
                    p_bikou = ""
            elif "主な症状" in c_txt:
                if "無症状" in c_txt:
                    p_symptons = "症状なし"
                elif "非公表" in c_txt:
                    p_symptons = "非公表"
                else:
                    if (i - ken_num) == 1:
                        p_symptons = c_txt.replace("主な症状等  ","").replace("、",";")
                    elif  (i - ken_num) == 2:
                        p_symptons = str(csv_read_df.iloc[i-1,j]) + c_txt
                        p_symptons = p_symptons.replace("主な症状等 ","").replace("、",";")
                        
            elif "渡航歴" in c_txt:
                #ブロック最後の行なので書き込み用データフレームに1行を追加
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
            
    print(csv_df) 
    csv_df.to_csv(CSV_path + "\\list_sapporo_" + dt_mmdd + ".csv", index=None, encoding='CP932')
else:
    print("札幌の患者一覧無し") 