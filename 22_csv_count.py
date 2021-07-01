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

#==============CSVに集計を行う関数==============
c_filename = pdf_path + "\\csv_merge_" + dt_mmdd + ".csv" #市町村データを結合したCSV
csv_city = pd.read_csv(c_filename,encoding="SHIFT_JIS") #市町村患者一覧をデータフレームにする

d_sorachi = 0
d_ishikari = 0
d_shiribeshi = 0
d_iburi = 0
d_hidaka = 0
d_oshima = 0
d_hiyama = 0
d_kamikawa = 0
d_rumoi = 0
d_souya = 0
d_ohotuku = 0
d_tokachi = 0
d_kushiro = 0
d_nemuro = 0
d_shinkoukyoku_hikoukai = 0
d_sonota = 0

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
d_age_hikoukai = 0

d_man = 0
d_woman = 0
d_sex_hikoukai = 0
d_mushoujyou = 0
d_keishou = 0
d_tyoutoushou = 0
d_jyoushou = 0
d_status_hikoukai = 0

#========振興局ごとの陽性者数計算=============
df_shinkoukyoku = csv_city.groupby("居住地").agg({"居住地": ["count"]}) #居住地でグループ化してカウントする
for i in range(len(df_shinkoukyoku)):
    if "空知" in str(df_shinkoukyoku.index[i]):
        d_sorachi += int(df_shinkoukyoku.iloc[i,0])
    elif "石狩" in str(df_shinkoukyoku.index[i]):
        d_ishikari += int(df_shinkoukyoku.iloc[i,0])
    elif "後志" in str(df_shinkoukyoku.index[i]):
        d_shiribeshi += int(df_shinkoukyoku.iloc[i,0])
    elif "胆振" in str(df_shinkoukyoku.index[i]):
        d_iburi += int(df_shinkoukyoku.iloc[i,0])
    elif "日高" in str(df_shinkoukyoku.index[i]):
        d_hidaka += int(df_shinkoukyoku.iloc[i,0])
    elif "渡島" in str(df_shinkoukyoku.index[i]):
        d_oshima += int(df_shinkoukyoku.iloc[i,0])
    elif "檜山" in str(df_shinkoukyoku.index[i]):
        d_hiyama += int(df_shinkoukyoku.iloc[i,0])
    elif "上川" in str(df_shinkoukyoku.index[i]):
        d_kamikawa += int(df_shinkoukyoku.iloc[i,0])
    elif "留萌" in str(df_shinkoukyoku.index[i]):
        d_rumoi += int(df_shinkoukyoku.iloc[i,0])
    elif "宗谷" in str(df_shinkoukyoku.index[i]):
        d_souya += int(df_shinkoukyoku.iloc[i,0])
    elif "オホーツク" in str(df_shinkoukyoku.index[i]):
        d_ohotuku += int(df_shinkoukyoku.iloc[i,0])
    elif "十勝" in str(df_shinkoukyoku.index[i]):
        d_tokachi += int(df_shinkoukyoku.iloc[i,0])
    elif "釧路" in str(df_shinkoukyoku.index[i]):
        d_kushiro += int(df_shinkoukyoku.iloc[i,0])
    elif "根室" in str(df_shinkoukyoku.index[i]):
        d_nemuro += int(df_shinkoukyoku.iloc[i,0])
    elif "非公表" in str(df_shinkoukyoku.index[i]):
        d_shinkoukyoku_hikoukai += int(df_shinkoukyoku.iloc[i,0])
    else:
        d_sonota += int(df_shinkoukyoku.iloc[i,0])

csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_shinkoukyoku_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする
day_total = d_sorachi+d_ishikari+d_shiribeshi+d_iburi+d_hidaka+d_oshima+d_hiyama+d_kamikawa+d_rumoi+d_souya+d_ohotuku+d_tokachi+d_kushiro+d_nemuro+d_sonota+d_shinkoukyoku_hikoukai
tmp_se = pd.Series(["北海道", d_sorachi,d_ishikari,d_shiribeshi,d_iburi,d_hidaka,d_oshima,d_hiyama,d_kamikawa,d_rumoi,d_souya,d_ohotuku,d_tokachi,d_kushiro,d_nemuro,d_sonota,d_shinkoukyoku_hikoukai,0,day_total ], index=csv_hokkaido.columns)
csv_hokkaido = csv_hokkaido.append(tmp_se, ignore_index = True)

#小樽のデータを追加
if(os.path.exists(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    df_otaru = pd.read_csv(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #小樽のデータをデータフレームにする
    #print("小樽0,0＝" + str(df_otaru.iloc[0,0]))
    otaru_total = int(df_otaru.iloc[0,0]) + int(df_otaru.iloc[0,1])
    tmp_otaru_se = pd.Series(["北海道",0,0,int(df_otaru.iloc[0,0]),0,0,0,0,0,0,0,0,0,0,0,0,int(df_otaru.iloc[0,1]),0,otaru_total ], index=csv_hokkaido.columns)
    csv_hokkaido = csv_hokkaido.append(tmp_otaru_se, ignore_index = True)

df_total = csv_hokkaido.groupby("地域").sum() #振興局ごとに合計する
print(df_total)
df_total.to_csv(pdf_path + "\\day_total_shinkoukyoku_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")

#========年代ごとの陽性者数計算=============
df_age = csv_city.groupby("年代").agg({"年代": ["count"]}) #年代でグループ化してカウントする
for i in range(len(df_age)):
    if "10歳未満" in str(df_age.index[i]):
        d_age01 += int(df_age.iloc[i,0])
    elif "10代" in str(df_age.index[i]):
        d_age10 += int(df_age.iloc[i,0])
    elif "20代" in str(df_age.index[i]):
        d_age20 += int(df_age.iloc[i,0])
    elif "30代" in str(df_age.index[i]):
        d_age30 += int(df_age.iloc[i,0])
    elif "40代" in str(df_age.index[i]):
        d_age40 += int(df_age.iloc[i,0])
    elif "50代" in str(df_age.index[i]):
        d_age50 += int(df_age.iloc[i,0])
    elif "60代" in str(df_age.index[i]):
        d_age60 += int(df_age.iloc[i,0])
    elif "70代" in str(df_age.index[i]):
        d_age70 += int(df_age.iloc[i,0])
    elif "80代" in str(df_age.index[i]):
        d_age80 += int(df_age.iloc[i,0])
    elif "90代" in str(df_age.index[i]):
        d_age90 += int(df_age.iloc[i,0])
    elif "100代" in str(df_age.index[i]):
        d_age90 += int(df_age.iloc[i,0])
    elif "非公表" in str(df_age.index[i]):
        d_age_hikoukai += int(df_age.iloc[i,0])
    else:
        d_age_hikoukai += int(df_age.iloc[i,0])

csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_age_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする
day_total = d_age01+d_age10+d_age20+d_age30+d_age40+d_age50+d_age60+d_age70+d_age80+d_age90+d_age_hikoukai
tmp_se = pd.Series(["北海道", d_age01,d_age10,d_age20,d_age30,d_age40,d_age50,d_age60,d_age70,d_age80,d_age90,d_age_hikoukai,0,day_total ], index=csv_hokkaido.columns)
csv_hokkaido = csv_hokkaido.append(tmp_se, ignore_index = True)

#小樽のデータを追加
if(os.path.exists(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    df_otaru = pd.read_csv(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #小樽のデータをデータフレームにする
    tmp_otaru_se = pd.Series(["北海道", 0,0,0,0,0,0,0,0,0,0,int(df_otaru.iloc[0,8]),0,int(df_otaru.iloc[0,8])], index=csv_hokkaido.columns)
    csv_hokkaido = csv_hokkaido.append(tmp_otaru_se, ignore_index = True)

df_total = csv_hokkaido.groupby("地域").sum() #年代ごとに合計する
print(df_total)
df_total.to_csv(pdf_path + "\\day_total_age_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")

#========状態ごとの陽性者数計算=============
df_status = csv_city.groupby("現状").agg({"現状": ["count"]}) #現状でグループ化してカウントする
for i in range(len(df_status)):
    if "無症状" in str(df_status.index[i]):
        d_mushoujyou += int(df_status.iloc[i,0])
    elif "軽症" in str(df_status.index[i]):
        d_keishou += int(df_status.iloc[i,0])
    elif "中等症" in str(df_status.index[i]):
        d_tyoutoushou += int(df_status.iloc[i,0])
    elif "重症" in str(df_status.index[i]):
        d_jyoushou += int(df_status.iloc[i,0])
    elif "非公表" in str(df_status.index[i]):
        d_status_hikoukai += int(df_status.iloc[i,0])
    else:
        d_status_hikoukai += int(df_status.iloc[i,0])

csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_status_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする
day_total = d_mushoujyou+d_keishou+d_tyoutoushou+d_jyoushou+d_status_hikoukai
tmp_se = pd.Series(["北海道", d_mushoujyou,d_keishou,d_tyoutoushou,d_jyoushou,d_status_hikoukai,0,day_total ], index=csv_hokkaido.columns)
csv_hokkaido = csv_hokkaido.append(tmp_se, ignore_index = True)

#小樽のデータを追加
if(os.path.exists(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    df_otaru = pd.read_csv(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #小樽のデータをデータフレームにする
    otaru_total = int(df_otaru.iloc[0,4]) + int(df_otaru.iloc[0,5]) + int(df_otaru.iloc[0,6]) + int(df_otaru.iloc[0,7])
    tmp_otaru_se = pd.Series(["北海道", int(df_otaru.iloc[0,4]) ,int(df_otaru.iloc[0,5]) ,int(df_otaru.iloc[0,6]) ,int(df_otaru.iloc[0,7]) ,0,0,otaru_total], index=csv_hokkaido.columns)
    csv_hokkaido = csv_hokkaido.append(tmp_otaru_se, ignore_index = True)

df_total = csv_hokkaido.groupby("地域").sum() #状態ごとに合計する
print(df_total)
df_total.to_csv(pdf_path + "\\day_total_status_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")

#========性別ごとの陽性者数計算=============
df_sex = csv_city.groupby("性別").agg({"性別": ["count"]}) #性別でグループ化してカウントする
for i in range(len(df_sex)):
    if "男性" in str(df_sex.index[i]):
        d_man  += int(df_sex.iloc[i,0])
    elif "女性" in str(df_sex.index[i]):
        d_woman += int(df_sex.iloc[i,0])
    elif "非公表" in str(df_sex.index[i]):
        d_sex_hikoukai += int(df_sex.iloc[i,0])
    else:
        d_sex_hikoukai += int(df_sex.iloc[i,0])

csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_sex_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする
day_total = d_man + d_woman+ d_sex_hikoukai
tmp_se = pd.Series(["北海道", d_man,d_woman,d_sex_hikoukai,0,day_total ], index=csv_hokkaido.columns)
csv_hokkaido = csv_hokkaido.append(tmp_se, ignore_index = True)

#小樽のデータを追加
if(os.path.exists(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    df_otaru = pd.read_csv(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #小樽のデータをデータフレームにする
    otaru_total = int(df_otaru.iloc[0,2]) + int(df_otaru.iloc[0,3])
    tmp_otaru_se = pd.Series(["北海道", int(df_otaru.iloc[0,2]) ,int(df_otaru.iloc[0,3]) ,0,0,otaru_total], index=csv_hokkaido.columns)
    csv_hokkaido = csv_hokkaido.append(tmp_otaru_se, ignore_index = True)

df_total = csv_hokkaido.groupby("地域").sum() #性別ごとに合計する
print(df_total)
df_total.to_csv(pdf_path + "\\day_total_sex_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")