import os
from numpy import False_
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

if(os.path.exists(CSV_path + "\\hokkaido_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    #pandasでCSVファイルを読み込み
    csv_old_df = pd.read_csv(CSV_path + "\\hokkaido_" + dt_mmdd + ".csv",encoding="CP932")
    #1つの列に2つのデータが有る場合があるので、CSVを修正したデータフレームを作成
    csv_read_df = pd.DataFrame()
    myFLG = False

    #1行目のヘッダ行を追加
    read_se = pd.Series(["No","例目","居住地","国籍","性別","年代","職業","現状","発症日","陽性確定日","現在の状況","患者との接触等"])
    csv_read_df = csv_read_df.append(read_se, ignore_index = True)

    for i in range(len(csv_old_df)-1):
        if "累計" in str(csv_old_df.iloc[i,0]):
            myFLG = True #患者一覧以外はそのまま複写

        mylist = [] #リストを初期化
        my_arr = []
        if myFLG == False: #患者一覧の場合
            if str(csv_old_df.iloc[i,0]) == "nan": #1列目が空白は処理しない
                dammy=1
            elif "No" in str(csv_old_df.iloc[i,0]): #1列目が「No」は処理しない
                dammy=1
            else:
                for j in range(len(csv_old_df.columns)):
                    myData = str(csv_old_df.iloc[i,j]) 
                    if "(" in myData : #「(」が含まれる場合は、「(」から右を削除
                        myData = myData[:myData.find("(")]
                    if " " in myData: #半角スペースがある場合、リストに変換
                        my_arr = myData.split(" ") #スペースで区切り配列を作る
                        for k in my_arr:
                            if k != "":
                                mylist.append(k)
                    elif myData == "nan" or myData == "": #データが空白の場合は処理しない
                        dammy=1
                    else:
                        mylist.append(myData) 
                    my_arr = [] #要素が1つならクリア
                #データを追加
                read_se = pd.Series(mylist)
                csv_read_df = csv_read_df.append(read_se, ignore_index = True)
     
        else:
            #患者一覧以外の場合はそのまま追加
            for j in range(len(csv_old_df.columns)):
                mylist.append(str(csv_old_df.iloc[i,j]))
            #データを追加           
            read_se = pd.Series(mylist)
            csv_read_df = csv_read_df.append(read_se, ignore_index = True)

    csv_read_df.to_csv(CSV_path + "\\hokkaido_New_" + dt_mmdd + ".csv", index=None, encoding="CP932")
    
    #データフレームを作成（カラムのみ指定） 参考ページ【https://qiita.com/567000/items/d8a29bb7404f68d90dd4】
    csv_df = pd.DataFrame( columns=["例目","年代","性別","居住地","職業","現状","補足","再陽性FG","発症日","発症年月日","症状元","患者_症状","渡航FG","備考","エラー"])

    #行の検査用
    ken_num = 0
    df_FLG = True
    no_kokuseki = 0
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_read_df)-1):
        if "累計" in str(csv_read_df.iloc[i,0]):
            df_FLG = False #累計検査数の行でフラグ終了

        if df_FLG : #フラグが立っている間の処理
            if "例目" in str(csv_read_df.iloc[i,1]): #「例目」以外なら処理
                p_error = ""
            elif str(csv_read_df.iloc[i,0]) != "nan" :
                p_num = str(csv_read_df.iloc[i,1])  #例目
                p_residence = str(csv_read_df.iloc[i,2])  #居住地

                p_error = ""
                #居住地を振興局に変換
                if "石狩" in p_residence or "札幌市" in p_residence:
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

                p_sex = str(csv_read_df.iloc[i,4])  #性別
                p_age = str(csv_read_df.iloc[i,5])  #年齢
                
                if "未満" in p_age : #10歳未満か判別
                    p_age = "10歳未満"
                else:
                    p_age = p_age.replace("歳","")
                p_job = str(csv_read_df.iloc[i,6])  #職業
                p_status = str(csv_read_df.iloc[i,7])  #現状
                c_hassho = str(csv_read_df.iloc[i,8])  #発症日
                
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
                if "再陽性" in str(csv_read_df.iloc[i,11]):
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

        #==========covid19_data.csv用のデータ============
        #累計検査数と陽性累計と現在患者数と軽症・中等症が一つになっている場合
        if "軽症・中等症" in str(csv_read_df.iloc[i,0]):
            kensa_arr = str(csv_read_df.iloc[i+1,0]).split(" ") #累計検査数、陽性累計、現在患者数、軽症中等症
            ruikei_arr.append(kensa_arr[0]) #累計検査数
            ruikei_arr.append(kensa_arr[1]) #陽性累計
            ruikei_arr.append(kensa_arr[2]) #現在患者数
            ruikei_arr.append(kensa_arr[3])  #軽症・中等症
            if str(csv_read_df.iloc[i+1,1])=="nan": #重  症  2列めか3列目にデータがあるので空白でない方を取得
                ruikei_arr.append(str(csv_read_df.iloc[i+1,2]))
            else:
                ruikei_arr.append(str(csv_read_df.iloc[i+1,1]))

            ruikei_arr.append(str(csv_read_df.iloc[i+1,3])) #死亡累計
            ruikei_arr.append(str(csv_read_df.iloc[i+1,4])) #陰性確認済み累計

        #累計検査数と陽性累計と現在患者数が一つになっている場合
        if str(csv_read_df.iloc[i,1]) == "軽症・中等症":
            kensa_arr = str(csv_read_df.iloc[i+1,0]).split(" ") #累計検査数、陽性累計、現在患者数
            ruikei_arr.append(kensa_arr[0]) #累計検査数
            ruikei_arr.append(kensa_arr[1]) #陽性累計
            ruikei_arr.append(kensa_arr[2]) #現在患者数
            retu = 1
            for num in range(4): #軽症・中等症、重症、死亡累計、陰性確認済み累計
                if str(csv_read_df.iloc[i+1,retu])=="nan":  #セルが空白なら次の列
                    retu = retu+1
                    ruikei_arr.append(str(csv_read_df.iloc[i+1,retu])) 
                    retu = retu+1
                else:
                    ruikei_arr.append(str(csv_read_df.iloc[i+1,retu])) 
                    retu = retu+1


        #累計検査数と陽性累計が一つになっている場合
        if str(csv_read_df.iloc[i,2]) == "軽症・中等症":
            kensa_arr = str(csv_read_df.iloc[i+1,0]).split(" ") #累計検査数、陽性累計
            ruikei_arr.append(kensa_arr[0]) #累計検査数
            ruikei_arr.append(kensa_arr[1]) #陽性累計
            retu = 1
            for num in range(5): #現在患者数、軽症・中等症、重症、死亡累計、陰性確認済み累計
                if str(csv_read_df.iloc[i+1,retu])=="nan":  #セルが空白なら次の列
                    retu = retu+1
                    ruikei_arr.append(str(csv_read_df.iloc[i+1,retu])) 
                    retu = retu+1
                else:
                    ruikei_arr.append(str(csv_read_df.iloc[i+1,retu])) 
                    retu = retu+1

        #累計検査数と陽性累計が別になっている場合    
        if str(csv_read_df.iloc[i,3]) == "軽症・中等症":
            retu = 0
            for num in range(7): #累計検査数、陽性累計、現在患者数、軽症・中等症、重症、死亡累計、陰性確認済み累計
                if str(csv_read_df.iloc[i+1,retu])=="nan":  #セルが空白なら次の列
                    retu = retu+1
                    ruikei_arr.append(str(csv_read_df.iloc[i+1,retu])) 
                    retu = retu+1
                else:
                    ruikei_arr.append(str(csv_read_df.iloc[i+1,retu])) 
                    retu = retu+1

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
        elif str(csv_read_df.iloc[i,1]) == "の新規患者数":
            ruikei_arr.append(str(csv_read_df.iloc[i+1,1])) #濃厚接触者等の新規患者数
            ruikei_arr.append(str(csv_read_df.iloc[i+1,2])) #濃厚接触者等以外の新規患者数

        #ステージ
        if "現時点における北海道" in str(csv_read_df.iloc[i,0]):
            d_stage = str(csv_read_df.iloc[i,0]).replace("3 現時点における北海道の状況 [ステージ","")
            d_stage = d_stage.replace("]","")
            ruikei_arr.append(d_stage) #ステージ
    if len(ruikei_arr) == 10:
        ruikei_arr.append("0") #ステージ
        
    print(ruikei_arr)        
    #covid19_data.csv用のデータを数値に変換
    for k in range(len(ruikei_arr)):
        ruikei_arr[k] = int(ruikei_arr[k].replace(",","").replace(".0","") )
    print(ruikei_arr)

    print(csv_df) 
    csv_df.to_csv(CSV_path + "\\list_hokkaido_" + dt_mmdd + ".csv", index=None, encoding="CP932")
    
    csv2_df = pd.DataFrame( columns=["累計検査数","陽性累計","現在患者数","軽症中等症","重症","死亡者累計","陰性累計","検査数","濃厚接触者数","濃厚以外数","ステージ"])
    tmp_se2 = pd.Series([ ruikei_arr[0], ruikei_arr[1], ruikei_arr[2], ruikei_arr[3], ruikei_arr[4], ruikei_arr[5], ruikei_arr[6], ruikei_arr[7], ruikei_arr[8], ruikei_arr[9], ruikei_arr[10]], index=csv2_df.columns)
    csv2_df = csv2_df.append(tmp_se2, ignore_index = True)
    csv2_df.to_csv(CSV_path + "\\ruikei_" + dt_mmdd + ".csv", index=None, encoding="CP932")

else:
    print("道庁まとめの患者一覧無し") 