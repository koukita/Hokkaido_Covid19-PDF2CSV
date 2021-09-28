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

#==============PDFをCSVに変換する関数==============
dt_mmdd = file_day.f_today()
dt_yesterday_mmdd = file_day.f_yesterday()
print("今日は" + dt_mmdd)

def pdf2csv(cityname,hyou,cja_name):
    #拡張子を除いたパス
    if cityname == "hakodate_":
        p_filename = pdf_path + "\\" + cityname + dt_mmdd + "a"
        if(os.path.exists(p_filename + ".pdf")) == False:
            p_filename = pdf_path + "\\" + cityname + dt_mmdd #「a」がついていない場合
    elif cityname == "hokkaido_nyuin_":
        p_filename = pdf_path + "\\" + cityname + dt_yesterday_mmdd
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
        if p_filename[-1] == "a": #一番最後の文字が「a」の場合（函館）は「a」を除去
            p_filename = p_filename[:-1]

        if cja_name=="北海道確保病床":
            #確保病床数用
            dfc.to_csv(p_filename + "_byoushou.csv", index=None, encoding="CP932")
        else:
            dfc.to_csv(p_filename + ".csv", index=None, encoding="CP932")
    else:
        print(cja_name + "のファイル無し")

#==============報道発表PDFをCSVに変換=================
#pdf2csv("hokkaido_","lattice","北海道")
pdf2csv("hokkaido_","stream","北海道")
pdf2csv("hokkaido_nyuin_","lattice","北海道入院") #入院属性用＿昨日のデータ
pdf2csv("hokkaido_nyuin_","stream","北海道確保病床") #入院属性用＿昨日のデータ
pdf2csv("sapporo_","stream","札幌")
pdf2csv("asahikawa_","stream","旭川")
pdf2csv("hakodate_","lattice","函館")
#pdf2csv("hakodate_","stream","函館")
pdf2csv("otaru_","lattice","小樽")
