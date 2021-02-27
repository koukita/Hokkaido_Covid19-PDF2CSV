import os
import pandas as pd
import tabula
import file_day
import pdf_download_path
from datetime import datetime, date, timedelta

#昨日の日付
today = datetime.today()
dt_mmdd = file_day.f_yesterday()
print("昨日は" + dt_mmdd)

#PDFのフォルダを指定
pdf_path = pdf_download_path.p_path()

#==============患者一覧=================
#PDFを読み込む
if(os.path.exists(pdf_path + "\\hasseijyoukyouitiran" + dt_mmdd + ".pdf")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    dfs = tabula.read_pdf(pdf_path + "\\hasseijyoukyouitiran" + dt_mmdd + ".pdf", lattice=True , pages = 'all')
    #結合用データフレームを１つ目のデータフレームで作成
    dfc = dfs[0]
    #データフレームの数、繰り返す（ただし２番めから）
    for df in dfs[1:99999]:
        #データフレームを行結合
        dfc = pd.concat([dfc,df])
    #列名を再設定
    dfc.columns = ["No","公表日","年代","性別","居住地","発生","状況"]
    #Noで並び替え
    df_so = dfc.sort_values("No")
    # CSVで出力
    df_so.to_csv(pdf_path + "\\hasseijyoukyouitiran" + dt_mmdd + ".csv", index=None, encoding="CP932")
    print("hasseijyoukyouitiran" + dt_mmdd + ".csv 患者一覧作成成功")
else:
    print("患者一覧ファイル無し")


#==============PDFをCSVに変換する関数==============
dt_mmdd = file_day.f_today()
print("今日は" + dt_mmdd)

def pdf2csv(cityname,hyou,cja_name):
    #拡張子を除いたパス
    if cityname == "hakodate_":
        p_filename = pdf_path + "\\" + cityname + dt_mmdd + "a"
    else:
        p_filename = pdf_path + "\\" + cityname + dt_mmdd
    
    if(os.path.exists(p_filename + ".pdf")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        print(cja_name + "今日は" + dt_mmdd)
        if hyou == "lattice": #「lattice=True」
            #罫線の表を取得
            dfs = tabula.read_pdf(p_filename + ".pdf", lattice=True, pandas_options={"header": None} , pages = 'all')
        else: #「stream=True」
            dfs = tabula.read_pdf(p_filename + ".pdf", stream=True, pandas_options={"header": None} , pages = 'all')
        
        #結合用データフレームに１つ目のデータフレームを導入
        dfc = dfs[0]
        #データフレームの数、繰り返す（ただし２番めから）
        for df in dfs[1:99999]:
            #データフレームを行結合
            dfc = pd.concat([dfc,df])
            #print(df)   
        # CSVで出力
        dfc.to_csv(p_filename + ".csv", index=None, encoding="CP932")
    else:
        print(cja_name + "のファイル無し")

#==============報道発表PDFをCSVに変換=================
pdf2csv("hokkaido_z","lattice","北海道")
pdf2csv("sapporo_","stream","札幌")
pdf2csv("asahikawa_","stream","旭川")
#pdf2csv("hakodate_","stream","函館")
pdf2csv("hakodate_","lattice","函館")
pdf2csv("otaru_","lattice","小樽")
