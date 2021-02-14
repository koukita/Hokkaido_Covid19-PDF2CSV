# 北海道公開の新型コロナウイルス情報「報道発表資料」PDFファイルをオープンデータCSVに変換するPythonプログラム
## はじめに
 このPythonプログラムは、北海道が毎日公表している、道内の新型コロナウイルス情報の報道発表資料のPDFファイルをオープンデータで公表しているCSVファイルに変換するプログラムです。  
　・北海道報道発表資料  
 　　http://www.pref.hokkaido.lg.jp/hf/kth/kak/hasseijoukyou.htm  
　・北海道オープンデータポータル  
 　　https://www.harp.lg.jp/opendata/dataset/1369.html  

## 変換に必要なファイル
    hasseijyoukyouitiranXXXX.pdf（必須）  
    hokkaido_zXXXXX.pdf  
    sapporo_XXXX.pdf  
    asahikawa_XXXX.pdf  
    hakodate_XXXX.pdf  
    otaru_XXXX.pdf  
※全てのファイルが必要ではありません。（「XXXX」は発表日）  
※PDFファイルを一つのフォルダにまとめてダウンロードしておきます。

## プログラムファイル
　プログラムファイルは、全て同じフォルダに保存しておきます。  
　このPythonプログラムは、Windows用に作っています。パスの指定などがOSごとに違う場合がありますので、適宜修正してください。
 
## 必要なPythonライブラリ
　このプログラムを実行するためには、次のライブラリが必要です。  
  Pythonに標準で組み込まれているものもありますが、足りないものは、各自インストールしてください。

  ・os  
  ・Pandas  
  ・Tabula  
  ・Datetime  
  

## パスの設定
　プログラムを実行する前に、ダウンロードされたPDFファイルのパスと、作成したCSVファイルを保存するパスの設定が必要です。  
　pdf_download_path.py をテキストエディタなどで開いて、「pdf_path = 」の部分にパスを設定してください。
 
 
## プログラムの実行
 Windowsの場合、「00_pdf2csv.bat」を実行すると、「csv_merge_XXXX.csv」を作成するプログラムが順番に実行され、PDFと同じフォルダにCSVファイルが作成されます。  
 ※「sapporo_XXXX.csv」「hokkaido_zXXXX.csv」などは、PDFをTabulaでCSVに変換し、pandasのデータフレームとしてCSV保存したものです。  
 　「list_sapporo_XXXX.csv」「list_hokkaido_XXXX.csv」などは、上記ファイルから患者一覧のみ抜き出したものです。  
  　これらは作業ファイルですので、データが正しく作成されていれば、削除してもOKです。  
  
 作成された「csv_merge_0214.csv」を確認し、データが正しければ、「30_公開用データ作成.bat」を実行します。  
 「自動作成ファイル」フォルダに、次の3つのファイルが作成されます。  
 
    ・010006_hokkaido_covid19_patients.csv（オープンデータ定義書に準拠した陽性患者一覧）  
    ・patients.csv（北海道独自の陽性患者一覧）  
    ・patients_age_sex.csv（日毎の年齢別、性別の陽性数累計）  
 
