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

#累計用の配列を用意
ruikei_arr =[]

if(os.path.exists(CSV_path + "\\hokkaido_z" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    #pandasでCSVファイルを読み込み
    csv_read_df = pd.read_csv(CSV_path + "\\hokkaido_z" + dt_mmdd + ".csv",encoding="CP932")
    #データフレームを作成（カラムのみ指定） 参考ページ【https://qiita.com/567000/items/d8a29bb7404f68d90dd4】
    csv_df = pd.DataFrame( columns=["例目","年代","性別","居住地","職業","現状","補足","再陽性FG","発症日","発症年月日","症状元","患者_症状","渡航FG","備考","エラー"])

    #行の検査用
    ken_num = 0
    df_FLG = False
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_read_df)-1):
        if df_FLG and str(csv_read_df.iloc[i,1])!="nan": #フラグが立っている間の処理
            p_num = str(csv_read_df.iloc[i,1])  #例目
            p_residence = str(csv_read_df.iloc[i,2])  #居住地
            p_error = ""
            #居住地を振興局に変換
            if "石狩" in p_residence:
                p_residence = "石狩振興局管内"
            elif "空知" in p_residence:
                p_residence = "空知総合振興局管内"
            elif "後志" in p_residence:
                p_residence = "後志総合振興局管内"
            elif "渡島" in p_residence:
                p_residence = "渡島総合振興局管内"
            elif "檜山" in p_residence:
                p_residence = "檜山振興局管内"
            elif "胆振" in p_residence:
                p_residence = "胆振総合振興局管内"
            elif "日高" in p_residence:
                p_residence = "日高振興局管内"
            elif "上川" in p_residence:
                p_residence = "上川総合振興局管内"
            elif "留萌" in p_residence:
                p_residence = "留萌振興局管内"
            elif "宗谷" in p_residence:
                p_residence = "宗谷総合振興局管内"
            elif "オホーツク" in p_residence:
                p_residence = "オホーツク総合振興局管内"
            elif "十勝" in p_residence:
                p_residence = "十勝総合振興局管内"
            elif "釧路" in p_residence:
                p_residence = "釧路総合振興局管内"
            elif "根室" in p_residence:
                p_residence = "根室振興局管内"
            elif "非公表" in p_residence:
                p_residence = "非公表"
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
            c_hassho = str(csv_read_df.iloc[i,9])  #発症日
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
        if str(csv_read_df.iloc[i,0]) == "No":
            #「No」の次の行からフラグをたてる
            df_FLG = True
        elif str(csv_read_df.iloc[i+1,10]) == "nan":
            #11列目が空白の場合はフラグを終了
            df_FLG = False

        #==========covid19_data.csv用のデータ============
        #累計検査数と陽性累計と現在患者数が一つになっている場合
        if str(csv_read_df.iloc[i,1]) == "軽症・中等症":
            kensa_arr = str(csv_read_df.iloc[i+1,0]).split(" ") #累計検査数、陽性累計、現在患者数
            ruikei_arr.append(kensa_arr[0]) #累計検査数
            ruikei_arr.append(kensa_arr[1]) #陽性累計
            ruikei_arr.append(kensa_arr[2]) #現在患者数
            ruikei_arr.append(str(csv_read_df.iloc[i+1,1])) #軽症・中等症
            ruikei_arr.append(str(csv_read_df.iloc[i+1,2])) #重  症
            ruikei_arr.append(str(csv_read_df.iloc[i+1,3])) #死亡累計
            ruikei_arr.append(str(csv_read_df.iloc[i+1,4])) #陰性確認済み累計

        #累計検査数と陽性累計が一つになっている場合
        if str(csv_read_df.iloc[i,2]) == "軽症・中等症":
            kensa_arr = str(csv_read_df.iloc[i+1,0]).split(" ") #累計検査数、陽性累計
            ruikei_arr.append(kensa_arr[0]) #累計検査数
            ruikei_arr.append(kensa_arr[1]) #陽性累計
            ruikei_arr.append(str(csv_read_df.iloc[i+1,1])) #現在患者数
            ruikei_arr.append(str(csv_read_df.iloc[i+1,2])) #軽症・中等症
            ruikei_arr.append(str(csv_read_df.iloc[i+1,3])) #重  症
            ruikei_arr.append(str(csv_read_df.iloc[i+1,4])) #死亡累計
            ruikei_arr.append(str(csv_read_df.iloc[i+1,5])) #陰性確認済み累計

        #累計検査数と陽性累計が別になっている場合    
        if str(csv_read_df.iloc[i,3]) == "軽症・中等症":
            ruikei_arr.append(str(csv_read_df.iloc[i+1,0])) #累計検査数
            ruikei_arr.append(str(csv_read_df.iloc[i+1,1])) #陽性累計
            ruikei_arr.append(str(csv_read_df.iloc[i+1,2])) #現在患者数
            ruikei_arr.append(str(csv_read_df.iloc[i+1,3])) #軽症・中等症
            ruikei_arr.append(str(csv_read_df.iloc[i+1,4])) #重  症
            ruikei_arr.append(str(csv_read_df.iloc[i+1,5])) #死亡累計
            ruikei_arr.append(str(csv_read_df.iloc[i+1,6])) #陰性確認済み累計

        #計と道分が1つになっている場合 
        if str(csv_read_df.iloc[i,0]) == "計 道分":
            kensa_arr=str(csv_read_df.iloc[i+1,0]).split(" ")
            ruikei_arr.append(kensa_arr[0]) #検査数実人数
        
        #計と道分が別になっている場合 
        if str(csv_read_df.iloc[i,1]) == "道分":
            ruikei_arr.append(str(csv_read_df.iloc[i+1,0])) #検査数実人数

        #新規患者と濃厚接触者数が１つになっている場合 
        if str(csv_read_df.iloc[i,0]) == "の新規患者数":
            kensa_arr=str(csv_read_df.iloc[i+1,0]).split(" ")
            ruikei_arr.append(kensa_arr[1])  #濃厚接触者等の新規患者数
            ruikei_arr.append(str(csv_read_df.iloc[i+1,1])) #濃厚接触者等以外の新規患者数
        
        #新規患者と濃厚接触者数が別になっている場合 
        if str(csv_read_df.iloc[i,1]) == "の新規患者数":
            ruikei_arr.append(str(csv_read_df.iloc[i+1,1])) #濃厚接触者等の新規患者数
            ruikei_arr.append(str(csv_read_df.iloc[i+1,2])) #濃厚接触者等以外の新規患者数

    #covid19_data.csv用のデータを数値に変換
    for k in range(len(ruikei_arr)):
        ruikei_arr[k] = int(ruikei_arr[k].replace(",","") )
    print(ruikei_arr)

    print(csv_df) 
    csv_df.to_csv(CSV_path + "\\list_hokkaido_" + dt_mmdd + ".csv", index=None, encoding="CP932")
    
    csv2_df = pd.DataFrame( columns=["累計検査数","陽性累計","現在患者数","軽症中等症","重症","死亡者累計","陰性累計","検査数","濃厚接触者数","濃厚以外数"])
    tmp_se2 = pd.Series([ ruikei_arr[0], ruikei_arr[1], ruikei_arr[2], ruikei_arr[3], ruikei_arr[4], ruikei_arr[5], ruikei_arr[6], ruikei_arr[7], ruikei_arr[8], ruikei_arr[9] ], index=csv2_df.columns)
    csv2_df = csv2_df.append(tmp_se2, ignore_index = True)
    csv2_df.to_csv(CSV_path + "\\ruikei_" + dt_mmdd + ".csv", index=None, encoding="CP932")

else:
    print("道庁まとめの患者一覧無し") 