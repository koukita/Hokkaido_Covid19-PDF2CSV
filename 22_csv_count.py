import os
import pandas as pd
import file_day
import pdf_download_path
from datetime import datetime, date, timedelta

print("＝＝＝＝22_csv_count.py＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝")
#今日の日付
today = datetime.today()
dt_mmdd = file_day.f_today()
print("今日は" + dt_mmdd)

pdf_path = pdf_download_path.p_path()

#==============CSVに集計を行う関数==============
if(os.path.exists(pdf_path + "\\day_hokkaido_shinkoukyoku_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】

    csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_shinkoukyoku_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする

    #札幌市のデータを追加 【2021/01/19 追加】
    if(os.path.exists(pdf_path + "\\day_sapporo_shinkoukyoku_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_sapporo = pd.read_csv(pdf_path + "\\day_sapporo_shinkoukyoku_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #札幌市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_sapporo])
        # print(csv_hokkaido)

    #旭川市のデータを追加 【2021/01/27 追加】
    if(os.path.exists(pdf_path + "\\day_asahikawa_shinkoukyoku_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_asahikawa = pd.read_csv(pdf_path + "\\day_asahikawa_shinkoukyoku_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #旭川市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_asahikawa])
        # print(csv_hokkaido)

    #函館市のデータを追加 【2021/01/26 追加】
    if(os.path.exists(pdf_path + "\\day_hakodate_shinkoukyoku_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_hakodate = pd.read_csv(pdf_path + "\\day_hakodate_shinkoukyoku_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #函館市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_hakodate])
        # print(csv_hokkaido)

    #小樽のデータを追加
    if(os.path.exists(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_otaru = pd.read_csv(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #小樽のデータをデータフレームにする
        #print("小樽0,0＝" + str(df_otaru.iloc[0,0]))
        otaru_total = int(df_otaru.iloc[0,0]) + int(df_otaru.iloc[0,1])
        tmp_otaru_se = pd.Series(["集計","小樽",0,0,int(df_otaru.iloc[0,0]),0,0,0,0,0,0,0,0,0,0,0,0,int(df_otaru.iloc[0,1]),0,otaru_total ], index=csv_hokkaido.columns)
        csv_hokkaido = csv_hokkaido.append(tmp_otaru_se, ignore_index = True)

    df_total = csv_hokkaido.groupby("集計").sum() #振興局ごとに合計する
    print(df_total)
    df_total.to_csv(pdf_path + "\\day_total_shinkoukyoku_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")

    #========年代ごとの陽性者数計算=============
    csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_age_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする

    #札幌市のデータを追加 【2021/01/19 追加】
    if(os.path.exists(pdf_path + "\\day_sapporo_age_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_sapporo = pd.read_csv(pdf_path + "\\day_sapporo_age_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #札幌市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_sapporo])
        #print(csv_hokkaido)

    #旭川市のデータを追加 【2021/01/27 追加】
    if(os.path.exists(pdf_path + "\\day_asahikawa_age_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_asahikawa = pd.read_csv(pdf_path + "\\day_asahikawa_age_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #旭川市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_asahikawa])
        # print(csv_hokkaido)

    #函館市のデータを追加 【2021/01/26 追加】
    if(os.path.exists(pdf_path + "\\day_hakodate_age_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_hakodate = pd.read_csv(pdf_path + "\\day_hakodate_age_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #函館市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_hakodate])
        # print(csv_hokkaido)

    #小樽のデータを追加
    if(os.path.exists(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_otaru = pd.read_csv(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #小樽のデータをデータフレームにする
        tmp_otaru_se = pd.Series(["集計","小樽", 0,0,0,0,0,0,0,0,0,0,int(df_otaru.iloc[0,8]),0,int(df_otaru.iloc[0,8])], index=csv_hokkaido.columns)
        csv_hokkaido = csv_hokkaido.append(tmp_otaru_se, ignore_index = True)

    df_total = csv_hokkaido.groupby("集計").sum() #年代ごとに合計する
    print(df_total)
    df_total.to_csv(pdf_path + "\\day_total_age_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")

    #========状態ごとの陽性者数計算=============
    csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_status_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする

    #札幌市のデータを追加 【2021/01/19 追加】
    if(os.path.exists(pdf_path + "\\day_sapporo_status_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_sapporo = pd.read_csv(pdf_path + "\\day_sapporo_status_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #札幌市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_sapporo])
        # print(csv_hokkaido)

    #旭川市のデータを追加 【2021/01/27 追加】
    if(os.path.exists(pdf_path + "\\day_asahikawa_status_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_asahikawa = pd.read_csv(pdf_path + "\\day_asahikawa_status_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #旭川市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_asahikawa])
        # print(csv_hokkaido)

    #函館市のデータを追加 【2021/01/26 追加】
    if(os.path.exists(pdf_path + "\\day_hakodate_status_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_hakodate = pd.read_csv(pdf_path + "\\day_hakodate_status_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #函館市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_hakodate])
        # print(csv_hokkaido)

    #小樽のデータを追加
    if(os.path.exists(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_otaru = pd.read_csv(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #小樽のデータをデータフレームにする
        otaru_total = int(df_otaru.iloc[0,4]) + int(df_otaru.iloc[0,5]) + int(df_otaru.iloc[0,6]) + int(df_otaru.iloc[0,7])
        tmp_otaru_se = pd.Series(["集計","小樽", int(df_otaru.iloc[0,4]) ,int(df_otaru.iloc[0,5]) ,int(df_otaru.iloc[0,6]) ,int(df_otaru.iloc[0,7]) ,0,0,otaru_total], index=csv_hokkaido.columns)
        csv_hokkaido = csv_hokkaido.append(tmp_otaru_se, ignore_index = True)

    df_total = csv_hokkaido.groupby("集計").sum() #状態ごとに合計する
    print(df_total)
    df_total.to_csv(pdf_path + "\\day_total_status_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")

    #========性別ごとの陽性者数計算=============
    csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_sex_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする

    #札幌市のデータを追加 【2021/01/19 追加】
    if(os.path.exists(pdf_path + "\\day_sapporo_sex_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_sapporo = pd.read_csv(pdf_path + "\\day_sapporo_sex_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #札幌市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_sapporo])
        # print(csv_hokkaido)

    #旭川市のデータを追加 【2021/01/27 追加】
    if(os.path.exists(pdf_path + "\\day_asahikawa_sex_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_asahikawa = pd.read_csv(pdf_path + "\\day_asahikawa_sex_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #旭川市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_asahikawa])
        # print(csv_hokkaido)

    #函館市のデータを追加 【2021/01/26 追加】
    if(os.path.exists(pdf_path + "\\day_hakodate_sex_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_hakodate = pd.read_csv(pdf_path + "\\day_hakodate_sex_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #函館市のデータをデータフレームにする
        csv_hokkaido = pd.concat([csv_hokkaido, df_hakodate])
        # print(csv_hokkaido)

    #小樽のデータを追加
    if(os.path.exists(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
        df_otaru = pd.read_csv(pdf_path + "\\day_otaru_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #小樽のデータをデータフレームにする
        otaru_total = int(df_otaru.iloc[0,2]) + int(df_otaru.iloc[0,3])
        tmp_otaru_se = pd.Series(["集計","小樽", int(df_otaru.iloc[0,2]) ,int(df_otaru.iloc[0,3]) ,0,0,otaru_total], index=csv_hokkaido.columns)
        csv_hokkaido = csv_hokkaido.append(tmp_otaru_se, ignore_index = True)

    df_total = csv_hokkaido.groupby("集計").sum() #性別ごとに合計する
    print(df_total)
    df_total.to_csv(pdf_path + "\\day_total_sex_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")
else:
    csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_shinkoukyoku_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする
    df_total = csv_hokkaido.groupby("集計").sum() #振興局ごとに合計する
    print(df_total)
    df_total.to_csv(pdf_path + "\\day_total_shinkoukyoku_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")

    csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_age_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする
    df_total = csv_hokkaido.groupby("集計").sum() #年代ごとに合計する
    print(df_total)
    df_total.to_csv(pdf_path + "\\day_total_age_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")

    csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_status_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする
    df_total = csv_hokkaido.groupby("集計").sum() #状態ごとに合計する
    print(df_total)
    df_total.to_csv(pdf_path + "\\day_total_status_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")

    csv_hokkaido = pd.read_csv(pdf_path + "\\day_hokkaido_sex_" + dt_mmdd + ".csv",encoding="SHIFT_JIS") #北海道振興局ごとデータをデータフレームにする
    df_total = csv_hokkaido.groupby("集計").sum() #性別ごとに合計する
    print(df_total)
    df_total.to_csv(pdf_path + "\\day_total_sex_" + dt_mmdd + ".csv",index=None,header=True, encoding="CP932")

