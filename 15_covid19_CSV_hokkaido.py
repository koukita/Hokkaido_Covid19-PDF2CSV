import os
from numpy import False_, floor
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

#累計用の配列を用意
ruikei_arr =[]

if(os.path.exists(CSV_path + "\\hokkaido_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    #pandasでCSVファイルを読み込み
    csv_old_df = pd.read_csv(CSV_path + "\\hokkaido_" + dt_mmdd + ".csv",encoding="CP932")
    #1つの列に2つのデータが有る場合があるので、CSVを修正したデータフレームを作成
    myFLG = False

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
    d_age100 = 0
    d_man = 0
    d_woman = 0
    d_mushoujyou = 0
    d_keishou = 0
    d_tyoutoushou = 0
    d_jyoushou = 0

    #=======振興局ごとの人数=======
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_old_df)-1):
        #合計が３列目にある前提
        if "空知" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_sorachi = int(shinkou_arr[0].replace(".0",""))
        if "石狩" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_ishikari = int(shinkou_arr[0].replace(".0",""))
        if "後志" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_shiribeshi = int(shinkou_arr[0].replace(".0",""))
        if "胆振" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_iburi = int(shinkou_arr[0].replace(".0",""))
        if "日高" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_hidaka = int(shinkou_arr[0].replace(".0",""))
        if "渡島" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_oshima = int(shinkou_arr[0].replace(".0",""))
        if "檜山" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_hiyama = int(shinkou_arr[0].replace(".0",""))
        if "上川" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_kamikawa = int(shinkou_arr[0].replace(".0",""))
        if "留萌" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_rumoi = int(shinkou_arr[0].replace(".0",""))
        if "宗谷" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_souya = int(shinkou_arr[0].replace(".0",""))
        if "オホーツク" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_ohotuku = int(shinkou_arr[0].replace(".0",""))
        if "十勝" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_tokachi = int(shinkou_arr[0].replace(".0",""))
        if "釧路" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_kushiro = int(shinkou_arr[0].replace(".0",""))
        if "根室" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            d_nemuro = int(shinkou_arr[0].replace(".0",""))
        if "その他" in str(csv_old_df.iloc[i,0]):
            shinkou_arr = str(csv_old_df.iloc[i,2]).split(" ") #2文字入っている場合は、配列に変換
            if shinkou_arr[0] == "nan":
                d_sonota = 0
            else:
                d_sonota = int(shinkou_arr[0].replace(".0",""))

        if "内道外" in str(csv_old_df.iloc[i,0]):
            break

    day_total = d_sorachi+d_ishikari+d_shiribeshi+d_iburi+d_hidaka+d_oshima+d_hiyama+d_kamikawa+d_rumoi+d_souya+d_ohotuku+d_tokachi+d_kushiro+d_nemuro+d_sonota
    #振興局別の患者数CSVを作成
    csv_shinkoukyoku_df = pd.DataFrame()
    read_se = pd.Series(["地域","空知","石狩","後志","胆振","日高","渡島","檜山","上川","留萌","宗谷","オホーツク","十勝","釧路","根室","道外他","非公表","重複削除","日計"])
    csv_shinkoukyoku_df = csv_shinkoukyoku_df.append(read_se, ignore_index = True)
    tmp_se = pd.Series(["北海道", d_sorachi,d_ishikari,d_shiribeshi,d_iburi,d_hidaka,d_oshima,d_hiyama,d_kamikawa,d_rumoi,d_souya,d_ohotuku,d_tokachi,d_kushiro,d_nemuro,d_sonota,0,0,day_total ], index=csv_shinkoukyoku_df.columns)
    csv_shinkoukyoku_df = csv_shinkoukyoku_df.append(tmp_se, ignore_index = True)
    print(csv_shinkoukyoku_df) 
    csv_shinkoukyoku_df.to_csv(CSV_path + "\\day_hokkaido_shinkoukyoku_" + dt_mmdd + ".csv",index=None,header=False, encoding="CP932")

    #=======年代ごとの人数=======
    for i in range(len(csv_old_df)-1):
        for j in range(len(csv_old_df.columns)):
            #合計が隣の列にある前提
            if "10歳未満" in str(csv_old_df.iloc[i,j]):
                age_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_age01 = int(age_arr[0].replace(".0",""))
            if "10歳代" in str(csv_old_df.iloc[i,j]):
                age_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_age10 = int(age_arr[0].replace(".0",""))
            if "20歳代" in str(csv_old_df.iloc[i,j]):
                age_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_age20 = int(age_arr[0].replace(".0",""))
            if "30歳代" in str(csv_old_df.iloc[i,j]):
                age_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_age30 = int(age_arr[0].replace(".0",""))
            if "40歳代" in str(csv_old_df.iloc[i,j]):
                age_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_age40 = int(age_arr[0].replace(".0",""))
            if "50歳代" in str(csv_old_df.iloc[i,j]):
                age_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_age50 = int(age_arr[0].replace(".0",""))
            if "60歳代" in str(csv_old_df.iloc[i,j]):
                age_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_age60 = int(age_arr[0].replace(".0",""))
            if "70歳代" in str(csv_old_df.iloc[i,j]):
                age_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_age70 = int(age_arr[0].replace(".0",""))
            if "80歳代" in str(csv_old_df.iloc[i,j]):
                age_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_age80 = int(age_arr[0].replace(".0",""))
            if "90歳" in str(csv_old_df.iloc[i,j]):
                age_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_age90 = int(age_arr[0].replace(".0",""))
                break
        if "90歳" in str(csv_old_df.iloc[i,j]):
            break

    day_total = d_age01+d_age10+d_age20+d_age30+d_age40+d_age50+d_age60+d_age70+d_age80+d_age90
    #年代別の患者数CSVを作成
    csv_age_df = pd.DataFrame()
    read_se = pd.Series(["地域","10歳未満","10歳代","20歳代","30歳代","40歳代","50歳代","60歳代","70歳代","80歳代","90歳代以上","非公表","重複削除","日計"])
    csv_age_df = csv_age_df.append(read_se, ignore_index = True)
    tmp_se = pd.Series(["北海道", d_age01,d_age10,d_age20,d_age30,d_age40,d_age50,d_age60,d_age70,d_age80,d_age90,0,0,day_total ], index=csv_age_df.columns)
    csv_age_df = csv_age_df.append(tmp_se, ignore_index = True)
    print(csv_age_df) 
    csv_age_df.to_csv(CSV_path + "\\day_hokkaido_age_" + dt_mmdd + ".csv",index=None,header=False, encoding="CP932")

    #=======状態ごとの人数=======
    for i in range(len(csv_old_df)-1):
        for j in range(len(csv_old_df.columns)):
            #合計が隣の列にある前提
            if "無症状" in str(csv_old_df.iloc[i,j]):
                status_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_mushoujyou = int(status_arr[0].replace(".0",""))
            if "軽症" in str(csv_old_df.iloc[i,j]):
                status_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_keishou = int(status_arr[0].replace(".0",""))
            if "中等症" in str(csv_old_df.iloc[i,j]):
                status_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_tyoutoushou = int(status_arr[0].replace(".0",""))
            if "重症" in str(csv_old_df.iloc[i,j]):
                status_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_jyoushou = int(status_arr[0].replace(".0",""))
                break
        if "重症" in str(csv_old_df.iloc[i,j]):
            break

    day_total = d_mushoujyou+d_keishou+d_tyoutoushou+d_jyoushou
    #状態別の患者数CSVを作成
    csv_status_df = pd.DataFrame()
    read_se = pd.Series(["地域","無症状","軽症","中等症","重症","非公表","重複削除","日計"])
    csv_status_df = csv_status_df.append(read_se, ignore_index = True)
    tmp_se = pd.Series(["北海道", d_mushoujyou,d_keishou,d_tyoutoushou,d_jyoushou,0,0,day_total ], index=csv_status_df.columns)
    csv_status_df = csv_status_df.append(tmp_se, ignore_index = True)
    print(csv_status_df) 
    csv_status_df.to_csv(CSV_path + "\\day_hokkaido_status_" + dt_mmdd + ".csv",index=None,header=False, encoding="CP932")

    #=======性別ごとの人数=======
    for i in range(len(csv_old_df)-1):
        for j in range(len(csv_old_df.columns)):
            #合計が隣の列にある前提
            if "男性" in str(csv_old_df.iloc[i,j]):
                sex_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_man = int(sex_arr[0].replace(".0",""))
            if "女性" in str(csv_old_df.iloc[i,j]):
                sex_arr = str(csv_old_df.iloc[i,j+1]).split(" ") #2文字入っている場合は、配列に変換
                d_woman = int(sex_arr[0].replace(".0",""))
                break
        if "女性" in str(csv_old_df.iloc[i,j]):
            break

    day_total = d_man + d_woman
    #性別別の患者数CSVを作成
    csv_sex_df = pd.DataFrame()
    read_se = pd.Series(["地域","男性","女性","非公表","重複削除","日計"])
    csv_sex_df = csv_sex_df.append(read_se, ignore_index = True)
    tmp_se = pd.Series(["北海道", d_man,d_woman,0,0,day_total ], index=csv_sex_df.columns)
    csv_sex_df = csv_sex_df.append(tmp_se, ignore_index = True)
    print(csv_sex_df) 
    csv_sex_df.to_csv(CSV_path + "\\day_hokkaido_sex_" + dt_mmdd + ".csv",index=None,header=False, encoding="CP932")

    #行の検査用
    ken_num = 0
    df_FLG = True
    no_kokuseki = 0
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_old_df)-1):
        #==========covid19_data.csv用のデータ============
        #累計検査数と陽性累計と現在患者数と軽症・中等症が一つになっている場合
        if "軽症・中等症" in str(csv_old_df.iloc[i,0]):
            kensa_arr = str(csv_old_df.iloc[i+1,0]).split(" ") #累計検査数、陽性累計、現在患者数、軽症中等症
            ruikei_arr.append(kensa_arr[0]) #累計検査数
            ruikei_arr.append(kensa_arr[1]) #陽性累計
            ruikei_arr.append(kensa_arr[2]) #現在患者数
            ruikei_arr.append(kensa_arr[3])  #軽症・中等症
            if str(csv_old_df.iloc[i+1,1])=="nan": #重  症  2列めか3列目にデータがあるので空白でない方を取得
                ruikei_arr.append(str(csv_old_df.iloc[i+1,2]))
            else:
                ruikei_arr.append(str(csv_old_df.iloc[i+1,1]))

            ruikei_arr.append(str(csv_old_df.iloc[i+1,3])) #死亡累計
            ruikei_arr.append(str(csv_old_df.iloc[i+1,4])) #陰性確認済み累計

        #累計検査数と陽性累計と現在患者数が一つになっている場合
        if str(csv_old_df.iloc[i,1]) == "軽症・中等症":
            kensa_arr = str(csv_old_df.iloc[i+1,0]).split(" ") #累計検査数、陽性累計、現在患者数
            ruikei_arr.append(kensa_arr[0]) #累計検査数
            ruikei_arr.append(kensa_arr[1]) #陽性累計
            ruikei_arr.append(kensa_arr[2]) #現在患者数
            retu = 1
            for num in range(4): #軽症・中等症、重症、死亡累計、陰性確認済み累計
                if str(csv_old_df.iloc[i+1,retu])=="nan":  #セルが空白なら次の列
                    retu = retu+1
                    ruikei_arr.append(str(csv_old_df.iloc[i+1,retu])) 
                    retu = retu+1
                else:
                    ruikei_arr.append(str(csv_old_df.iloc[i+1,retu])) 
                    retu = retu+1


        #累計検査数と陽性累計が一つになっている場合
        if str(csv_old_df.iloc[i,2]) == "軽症・中等症":
            kensa_arr = str(csv_old_df.iloc[i+1,0]).split(" ") #累計検査数、陽性累計
            ruikei_arr.append(kensa_arr[0]) #累計検査数
            ruikei_arr.append(kensa_arr[1]) #陽性累計
            retu = 1
            for num in range(5): #現在患者数、軽症・中等症、重症、死亡累計、陰性確認済み累計
                if str(csv_old_df.iloc[i+1,retu])=="nan":  #セルが空白なら次の列
                    retu = retu+1
                    ruikei_arr.append(str(csv_old_df.iloc[i+1,retu])) 
                    retu = retu+1
                else:
                    ruikei_arr.append(str(csv_old_df.iloc[i+1,retu])) 
                    retu = retu+1

        #累計検査数と陽性累計が別になっている場合    
        if str(csv_old_df.iloc[i,3]) == "軽症・中等症":
            retu = 0
            for num in range(7): #累計検査数、陽性累計、現在患者数、軽症・中等症、重症、死亡累計、陰性確認済み累計
                if str(csv_old_df.iloc[i+1,retu])=="nan":  #セルが空白なら次の列
                    retu = retu+1
                    ruikei_arr.append(str(csv_old_df.iloc[i+1,retu])) 
                    retu = retu+1
                else:
                    ruikei_arr.append(str(csv_old_df.iloc[i+1,retu])) 
                    retu = retu+1

        #計と道分が1つになっている場合 
        if str(csv_old_df.iloc[i,0]) == "計 道分":
            kensa_arr=str(csv_old_df.iloc[i+1,0]).split(" ")
            ruikei_arr.append(kensa_arr[0]) #検査数実人数
        
        #計と道分が別になっている場合 
        if str(csv_old_df.iloc[i,1]) == "道分":
            ruikei_arr.append(str(csv_old_df.iloc[i+1,0])) #検査数実人数

        #新規患者と濃厚接触者数が１つになっている場合 
        if str(csv_old_df.iloc[i,0]) == "の新規患者数":
            kensa_arr=str(csv_old_df.iloc[i+1,0]).split(" ")
            ruikei_arr.append(kensa_arr[1])  #濃厚接触者等の新規患者数
            ruikei_arr.append(str(csv_old_df.iloc[i+1,1])) #濃厚接触者等以外の新規患者数
        #新規患者と濃厚接触者数が別になっている場合 
        elif str(csv_old_df.iloc[i,1]) == "の新規患者数":
            ruikei_arr.append(str(csv_old_df.iloc[i+1,1])) #濃厚接触者等の新規患者数
            ruikei_arr.append(str(csv_old_df.iloc[i+1,2])) #濃厚接触者等以外の新規患者数

        #ステージ
        if "現時点における北海道" in str(csv_old_df.iloc[i,0]):
            d_stage = str(csv_old_df.iloc[i,0]).replace("3 現時点における北海道の状況 [ステージ","")
            d_stage = d_stage.replace("]","")
            ruikei_arr.append(d_stage) #ステージ
    if len(ruikei_arr) == 10:
        #シンプルダイアログの表示
        root = tk.Tk() 
        root.withdraw() #小さなウインドウを表示させない設定
        inputdata = simpleDialog.askstring("Input Box","ステージの数値を入力してください",)
        if inputdata == None:
            ruikei_arr.append("0") #ステージ
        else:
            ruikei_arr.append(inputdata) #ステージ
        
    print(ruikei_arr)        
    #covid19_data.csv用のデータを数値に変換
    for k in range(len(ruikei_arr)):
        ruikei_arr[k] = int(ruikei_arr[k].replace(",","").replace(".0","") )
    print(ruikei_arr)
    
    csv2_df = pd.DataFrame( columns=["累計検査数","陽性累計","現在患者数","軽症中等症","重症","死亡者累計","陰性累計","検査数","濃厚接触者数","濃厚以外数","ステージ"])
    tmp_se2 = pd.Series([ ruikei_arr[0], ruikei_arr[1], ruikei_arr[2], ruikei_arr[3], ruikei_arr[4], ruikei_arr[5], ruikei_arr[6], ruikei_arr[7], ruikei_arr[8], ruikei_arr[9], ruikei_arr[10]], index=csv2_df.columns)
    csv2_df = csv2_df.append(tmp_se2, ignore_index = True)
    csv2_df.to_csv(CSV_path + "\\ruikei_" + dt_mmdd + ".csv", index=None, encoding="CP932")

else:
    print("道庁まとめの患者一覧無し") 