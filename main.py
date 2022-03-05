
#-------------------------------------------------------
import importlib
import matplotlib.pyplot as plt
import PointClass
importlib.reload(PointClass)
from PointClass import Point

import random

import Pollution_Data_Reader
importlib.reload(Pollution_Data_Reader)
from Pollution_Data_Reader import PollutionDataReader

import Pickle_Reader
#----------------------------------------------------




#----------------------------------------------------------------------
def AnimatePollutionTimeChange(pollution, time_start, time_last, step):
    """濃度分布の時間変化をアニメ表示する"""
    for t_i in range(time_start, time_last, step):
        fig = plt.figure()
        graph = fig.add_subplot(111)
        #何秒時点の濃度分布を表示するか指定する必要がある
        graph = pollution.View(graph, time = t_i)
#-----------------------------------------------------------------------





#--------------------------------------------------------------
def AnimateMovingRoad(pollution, time_start, time_last, step, xList, yList, tList):
    """移動経路をアニメ表示する"""
    for t_i in range(time_start, time_last, step):
        fig = plt.figure()
        graph = fig.add_subplot(111)
        #この時点で濃度分布が描画される
        graph = pollution.View(graph, time = t_i)
        #表示したい部分より後の時刻の移動経路を無視する
        new_x, new_y = DeleteAfterTimeRoad(xList, yList, tList, t_i)
        #すでに濃度分布が描画されているグラフオブジェクトに、移動経路を上書き
        graph.scatter(new_x, new_y, c = 'red')
#-----------------------------------------------------------------




#------------------------------------------------------------------
def DeleteAfterTimeRoad(xList, yList, tList, time):
    """ある時刻より、あとに辿った座標を消す"""
    new_x = list()
    new_y = list()
    limit = len(xList)

    for i in range(limit):
        #定めた時間を超えていれば、無視する
        if(tList[i] > time):
            continue #for文のはじめにもどる

        #定めた時間を超えていなければ、その座標は残す
        new_x.append(xList[i])
        new_y.append(yList[i])

    return new_x, new_y
#-------------------------------------------------------------------






#-------------------------------------------------------------------
def main():
    """時間変化あり濃度分布モデル上での探索シミュレーションについての説明"""

    #1.濃度ファイルを読み出すための設定を行う（オブジェクト生成）
    #2.濃度ファイルが正しいか、そして正しく読み出せているか確認（アニメーション）
    #3.GetPollutionメソッドを使ってある座標及び時間での濃度値を取得
    #GetPollutionメソッドやViewメソッドがついていますが、PollutionDataReaderオブジェクトであり、Pollutionオブジェクトではありません
    #4.移動経路もできればアニメーションで確認する


    #ファイルの拡張子は必ずカンマありで指定してください
    #ファイルがなく、フォルダ名だけを指定してください。
    #PollutionFilesフォルダをみていただければわかるとおり、ファイル名で秒数を判別しています(引継ぎ資料を参照)
    pklReader = Pickle_Reader.PickleReader()
    pollutionDataReader = PollutionDataReader("PollutionFiles/", '.pkl', pklReader)

    #濃度分布モデルの読み出し確認。パラメータでアニメーションの開始時間や表示感覚を変更できます
    #重い処理なので省いていただいても大丈夫です
    #AnimatePollutionTimeChange(pollutionDataReader, time_start = 0, time_last = 50, step = 1)

    #ある座標および時間での濃度値を取得
    print("x = 0, y = 0, t = 50での濃度値")
    print(pollutionDataReader.GetPollution(x = 0, y = 0, t = 50))
    #濃度値は整数の座標および時刻で保存されていますが
    #時間に小数を指定した場合、補完が入り、濃度値を取得できます（座標は整数のみ）
    print("x = 0, y = 0, t = 50.33での濃度値")
    print(pollutionDataReader.GetPollution(x = 0, y = 0, t = 50.33))

    #移動経路をアニメーション表示する
    #表示用のダミーデータ（移動経路と時間）を作成
    #移動時間順に探索座標を記録することができている場合、アニメーション表示できる
    #例えば以下のリストは時間リスト（tList)の要素数が50, 座標も50個ずつで順番もきちんとそろっている
    xList = [random.uniform(0, 50) for x in range(50)] #ランダムな値を生成
    yList = [random.uniform(0, 50) for y in range(50)]
    tList = [t for t in range(50)] #50秒分

    AnimateMovingRoad(pollutionDataReader, time_start = 0, time_last = 50, step = 1, xList = xList, yList = yList, tList = tList)
#-----------------------------------------------------------------------
if __name__ == "__main__":
    main()
