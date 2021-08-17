import os
import pandas as pd
import file_day
import pdf_download_path
from datetime import datetime, date, timedelta
#数値入力用のシンプルダイアログの表示
import tkinter as tk
import tkinter.simpledialog as simpleDialog

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
    df_FLG = False
    no_kokuseki = 0
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_read_df)-1):
        if df_FLG and str(csv_read_df.iloc[i,1])!="nan": #フラグが立っている間の処理
            if "例目" in str(csv_read_df.iloc[i,1]): #「例目」以外なら処理
                p_error = ""
            else:
                p_num = str(csv_read_df.iloc[i,col_num])  #例目
                p_residence = str(csv_read_df.iloc[i,col_residence])  #居住地

                p_error = ""
                #居住地を振興局に変換
                if "石狩" in p_residence or "札幌市" in p_residence:
                    p_residence = "石狩振興局管内"
                elif "非公表" in p_residence:
                    p_residence = "非公表"
                else:
                    #シンプルダイアログの表示
                    root = tk.Tk() 
                    root.withdraw() #小さなウインドウを表示させない設定
                    inputdata = simpleDialog.askstring("Input Box",
                    "振興局名または道外の場合は都道府県名を入力してください。\n振興局の場合は「〇〇振興局管内」と入力します。\n居住地："
                    +p_residence,initialvalue=p_residence)
                    if inputdata == None:
                        p_residence = ""
                    else:
                        p_residence = inputdata

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

                p_job = str(csv_read_df.iloc[i,col_job])  #職業
                p_status = str(csv_read_df.iloc[i,col_status])  #現状
                if str(csv_read_df.iloc[i,col_hassho]) == "nan":
                    c_hassho = str(csv_read_df.iloc[i-1,col_hassho])  #空白ならひとつ上の行のデータを取得
                else:
                    c_hassho = str(csv_read_df.iloc[i,col_hassho])  #発症日
                
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
                elif "調査中" in c_hassho:
                    p_Hday = ""
                    p_bikou = "発症日は調査中"                
                else:
                    p_Hday = ""
                    p_bikou = ""
                p_symptons = "非公表" #症状
                if "再陽性" in str(csv_read_df.iloc[i+1,col_saiyousei]):
                    #次の行に再陽性と記載されている場合
                    p_saiyousei = "1"
                else:
                    p_saiyousei = "0"

                p_error = ""
                
                #配列にして、データフレームに追加
                #["例目","年代","性別","居住地","職業","現状","補足","再陽性FG","発症日","発症年月日","症状元","患者_症状","渡航FG","備考","エラー"])
                tmp_se = pd.Series([ p_num, p_age, p_sex, p_residence, p_job, p_status, "", p_saiyousei, "", p_Hday, "", p_symptons, "0", p_bikou, p_error ], index=csv_df.columns)
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
                    col_num = j
                if "居住地" in str(csv_read_df.iloc[i,j]):
                    col_residence = j 
                if "性別" in str(csv_read_df.iloc[i,j]):
                    col_sex = j
                if "年代" in str(csv_read_df.iloc[i,j]):
                    col_age = j
                if "職業" in str(csv_read_df.iloc[i,j]):
                    col_job = j
                if "現状" in str(csv_read_df.iloc[i,j]):
                    col_status = j
                if "発症日" in str(csv_read_df.iloc[i-1,j]):
                    col_hassho = j 
                if "接触者" in str(csv_read_df.iloc[i+1,j]):
                    col_saiyousei = j
            
        elif str(csv_read_df.iloc[i+1,1]) == "PCR":
            #B列に「PCR」と記入されていればフラグ終了
        # elif str(csv_read_df.iloc[i+1,no_kokuseki+6]) == "nan" and str(csv_read_df.iloc[i+1,no_kokuseki+7]) == "nan" and str(csv_read_df.iloc[i+1,no_kokuseki+8]) == "nan":
            #11列目(K)、12列名(L)、13列名(M)が空白の場合はフラグを終了
            df_FLG = False
            
    print(csv_df) 
    csv_df.to_csv(CSV_path + "\\list_sapporo_" + dt_mmdd + ".csv", index=None, encoding='CP932')
else:
    print("札幌の患者一覧無し") 