import os
from numpy import False_, floor
import pandas as pd
import file_day
import pdf_download_path
from datetime import datetime, date, timedelta
#数値入力用のシンプルダイアログの表示
import tkinter as tk
import tkinter.simpledialog as simpleDialog

#PDFをテキストに変換する「pdfminer.six」をインストールして使用する。
#【参考URL】https://www.shibutan-bloomers.com/python_library_pdfminer-six/2124/
# PDFファイルを読込んで、Pythonのコンソールに出力する
# 必要なPdfminer.sixモジュールのクラスをインポート
from pdfminer.pdfinterp import PDFResourceManager #PDFファイル内のコンテンツ（テキストや画像など）やその他リソースを管理する基幹クラス
from pdfminer.converter import TextConverter #PDFファイル内のテキストを抽出する機能を提供するクラス
from pdfminer.pdfinterp import PDFPageInterpreter #取得したPDFPageオブジェクトを解析する機能を提供
from pdfminer.pdfpage import PDFPage #ファイルからページ毎の個別情報を取得するジェネレーターを生成
from pdfminer.layout import LAParams #テキスト抽出解析に必要なPDFファイルのレイアウト情報をパラメーターとして設定するするためのクラス
from io import StringIO

#今日の日付
today = datetime.today()
dt_mmdd = file_day.f_yesterday()
print("今日は" + dt_mmdd)

#CSVのフォルダを指定
CSV_path = pdf_download_path.p_path()

#累計用の配列を用意
ruikei_arr =[]

if(os.path.exists(CSV_path + "\\hokkaido_nyuin_" + dt_mmdd + ".csv")): #ファイルが存在するか確認 参考【https://techacademy.jp/magazine/18994】
    
    #====PDFをtextに変換し、病床数を取得======
    # 標準組込み関数open()でモード指定をbinaryでFileオブジェクトを取得
    fp = open(CSV_path + "\\hokkaido_nyuin_" + dt_mmdd + ".pdf", 'rb')

    # 出力先をPythonコンソールするためにIOストリームを取得
    outfp = StringIO()

    # 各種テキスト抽出に必要なPdfminer.sixのオブジェクトを取得する処理
    rmgr = PDFResourceManager() # PDFResourceManagerオブジェクトの取得
    lprms = LAParams()          # LAParamsオブジェクトの取得
    device = TextConverter(rmgr, outfp, laparams=lprms)    # TextConverterオブジェクトの取得
    iprtr = PDFPageInterpreter(rmgr, device) # PDFPageInterpreterオブジェクトの取得

    # PDFファイルから1ページずつ解析(テキスト抽出)処理する
    for page in PDFPage.get_pages(fp):
        iprtr.process_page(page)

    text = outfp.getvalue()  # Pythonコンソールへの出力内容を取得

    outfp.close()  # I/Oストリームを閉じる
    device.close() # TextConverterオブジェクトの解放
    fp.close()     #  Fileストリームを閉じる

    #print(text)  # Jupyterの出力ボックスに表示する
    #確保病床数
    txt_find1 = text.find("病床数は") #病床数を抽出するためのはじめの文字位置
    txt_find2 = text.find("床（") #終わりの文字位置
    byousho1 = text[txt_find1+4:txt_find2].replace(",","") #文字の位置から病床数を抽出
    #重症用病床数
    txt_find1 = text.find("うち重症") #病床数を抽出するためのはじめの文字位置
    txt_find2 = text.find("床）") #終わりの文字位置
    byousho2 = text[txt_find1+4:txt_find2].replace(",","") #文字の位置から病床数を抽出

    byousho_arr = [byousho1,byousho2] #リストを作成
    #======病床数の取得はここまで======


    #pandasでCSVファイルを読み込み
    csv_old_df = pd.read_csv(CSV_path + "\\hokkaido_nyuin_" + dt_mmdd + ".csv",encoding="CP932")
    #CSVデータフレームを1行目から読み込む
    for i in range(len(csv_old_df)-1):
        #１列目に「全道」が含まれる行まで移動
        if "全道" in str(csv_old_df.iloc[i,0]):
            #改行コードで分割しリストに追加
            nyuin_arr1 = str(csv_old_df.iloc[i,1]).split("\r") #現在患者数
            nyuin_arr2 = str(csv_old_df.iloc[i,2]).split("\r") #入院患者
            nyuin_arr3 = str(csv_old_df.iloc[i,3]).split("\r") #宿泊療養施設入所者
            nyuin_arr4 = str(csv_old_df.iloc[i,4]).split("\r") #自宅療養者
            nyuin_arr5 = str(csv_old_df.iloc[i,5]).split("\r") #施設療養者
            nyuin_arr6 = str(csv_old_df.iloc[i,6]).split("\r") #調整中
            nyuin_arr= nyuin_arr1 + nyuin_arr2 + nyuin_arr3 + nyuin_arr4 + nyuin_arr5 + nyuin_arr6 + byousho_arr
            #print(nyuin_arr)
            #forを抜ける
            break
    
    nyuin_int_arr = [] #整数入力用のリストを準備
    #不要な文字「（ ）」を削除
    for i in range(len(nyuin_arr)): #リストの要素数分繰り返す
        new_text = nyuin_arr[i].replace("(","") #「（」を削除
        new_text = new_text.replace(")","") #「)」を削除
        new_text = new_text.replace("▲","-") #「▲」を「-」に置き換え
        new_text = new_text.replace("±","") #「▲」を「-」に置き換え
        new_text = new_text.replace("[","") #「[」を削除
        new_text = new_text.replace("]","") #「]」を削除
        new_text = new_text.replace(",","") #「,」を削除
        new_int = int(new_text) #整数値に変更
        nyuin_int_arr.append(new_int)

    
    #print(nyuin_int_arr)
    #入院属性を作成
    csv_nyuin_df = pd.DataFrame()
    read_se = pd.Series(["現在患者数","現在患者数（前日比）","入院患者","入院患者（前日比）","宿泊療養施設入所者","宿泊療養施設入所者（前日比）","自宅療養者","自宅療養者（前日比）","施設療養者","施設療養者（前日比）","調整中","調整中（前日比）","確保病床数","確保病床数（うち重症）"])
    csv_nyuin_df = csv_nyuin_df.append(read_se, ignore_index = True) #「ignore_index = True」はIndexを無視するという意味
    tmp_se = pd.Series(nyuin_int_arr, index=csv_nyuin_df.columns)
    csv_nyuin_df = csv_nyuin_df.append(tmp_se, ignore_index = True)
    print("=====入院患者属性=====")
    print(nyuin_int_arr) 
    csv_nyuin_df.to_csv(CSV_path + "\\day_hokkaido_nyuin_" + dt_mmdd + ".csv",index=None,header=False, encoding="CP932")


else:
    print("道庁まとめの患者一覧無し") 