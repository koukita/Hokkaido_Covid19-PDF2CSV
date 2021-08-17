import glob
import os
import file_day
import pdf_download_path
from datetime import datetime, date, timedelta

#昨日の日付
today = datetime.today()
dt_mmdd = file_day.f_today()
print("今日は" + dt_mmdd)
print("ファイル名を修正します")

#PDFのフォルダを指定
pdf_path = pdf_download_path.p_path()

#ファイル名の修正
#札幌
oldFileName = glob.glob(pdf_path + "\\*札幌市報道*.pdf") #「札幌市報道」を含むファイルを検索しリストに代入
newFileName = pdf_path + "\\sapporo_" + dt_mmdd + ".pdf"
if len(oldFileName) > 0:
    os.rename(oldFileName[0], newFileName) #ファイル名の変更

#函館
oldFileName = glob.glob(pdf_path + "\\*函館市報道*.pdf") #「函館市報道」を含むファイルを検索しリストに代入
newFileName = pdf_path + "\\hakodate_" + dt_mmdd + ".pdf"
if len(oldFileName) > 0:
    os.rename(oldFileName[0], newFileName) #ファイル名の変更

#小樽
oldFileName = glob.glob(pdf_path + "\\*小樽市報道*.pdf") #「小樽市報道」を含むファイルを検索しリストに代入
newFileName = pdf_path + "\\otaru_" + dt_mmdd + ".pdf"
if len(oldFileName) > 0:
    os.rename(oldFileName[0], newFileName) #ファイル名の変更

#旭川
oldFileName = glob.glob(pdf_path + "\\*旭川市報道*.pdf") #「旭川市報道」を含むファイルを検索しリストに代入
newFileName = pdf_path + "\\asahikawa_" + dt_mmdd + ".pdf"
if len(oldFileName) > 0:
    os.rename(oldFileName[0], newFileName) #ファイル名の変更

#北海道
oldFileName = glob.glob(pdf_path + "\\*新型コロナウイルスに関連した患者*.pdf") #キーワードを含むファイルを検索しリストに代入
newFileName = pdf_path + "\\hokkaido_" + dt_mmdd + ".pdf"
if len(oldFileName) > 0:
    os.rename(oldFileName[0], newFileName) #ファイル名の変更

print("ファイル名修正完了")

