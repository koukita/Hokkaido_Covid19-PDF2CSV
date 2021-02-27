import os
import pandas as pd
import file_day
import pdf_download_path
from datetime import datetime, date, timedelta

#今日の日付
today = datetime.today()
dt_mmdd = file_day.f_today()
print("今日は" + dt_mmdd)

pdf_path = pdf_download_path.p_path()

#==============CSVファイルが存在するか確認する関数==============
def csv2df(cityname):
    c_filename = pdf_path + "\\list_" + cityname + "_" + dt_mmdd + ".csv"
    if(os.path.exists(c_filename)): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        rdf = pd.read_csv(c_filename,encoding="SHIFT_JIS")
    else:
        rdf = pd.DataFrame()
        print(cityname + "のファイル無し")

    return rdf

#==============CSVの結合=================
csv_hakodate = csv2df("hakodate")
csv_sapporo = csv2df("sapporo")
csv_otaru = csv2df("otaru")
csv_asahikawa = csv2df("asahikawa")
csv_hokkaido = csv2df("hokkaido")

csv_df = pd.concat([csv_hakodate,csv_sapporo,csv_otaru,csv_asahikawa,csv_hokkaido])
print(csv_df)
df_so = csv_df.sort_values("例目")
print(df_so)
#順番が正しいか確認
check_no = int(df_so.iloc[0,0])-1
for i in range(len(df_so)):
    if check_no != int(df_so.iloc[i,0])-1:
        print("エラー！　No," + str(int(df_so.iloc[i,0])-1) + " がありません")
    
    #チェック用Noの更新
    check_no = int(df_so.iloc[i,0])
    

# CSVで出力
df_so.to_csv(pdf_path + "\\csv_merge_" + dt_mmdd + ".csv", index=None, encoding='shift-jis')
print("データの確認を行って、OKなら「30_公開用データ作成.bat」を実行してください")
