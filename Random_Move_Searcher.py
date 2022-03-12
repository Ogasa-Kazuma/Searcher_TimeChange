
import sys, os
import pandas as pd

class RandomMoveSearcher():

    def __init__(self, pollutionData, randomMoveScope, speed):
        #こうやってメンバ変数にしたほうが、メソッド呼び出しの引数が少なくてすむ
        #コンストラクタを呼ぶ回数とメソッドを呼ぶ回数で
        #引数の数をどちらを多くするか判断指標になるかも
        self.__pollutionData = pollutionData
        self.__distance_random_move_max = randomMoveScope
        self.__speed = speed


    def TargetPollutionValueOverPoint(self, point_start, time_range, targetPollutionValue):

        #より抽象なものに依存せよ
        #pollutionに依存しすぎてて再利用性低い気が
        #というかstraightLineにめっちゃ依存してる
        #straightLineのインターフェースを安定させる必要あり
        #依存先はpollutionDataReader, timeRange, point

        searchingData = self.SearchingData()
        point_now = point_start
        #なんか依存感
        time_now = time_range.GetStartTime()


        while(1):


            point_next = self.__DecideNextDirection(point_now)
            straightLine = self.__pollutionData.StraightLine(point_now, point_next, time_now, self.__speed)


            while(straightLine.HasNext()):
                point_i, t_i, pollution_i = straightLine.Next()
                searchingData.Append(point_i, t_i, pollution_i)

                if(time_range.IsTimeOver(t_i)):
                    #searchingDataにすることによって、pollution_iとかt_iとかがめっちゃまとまった！
                    return searchingData

                if(pollution_i >= targetPollutionValue):
                    return searchingData

                point_now = point_i
                time_now = t_i







    def __DecideNextDirection(self, point_base):

        while(1):
            point_next = self.__pollutionData.RandomPoint()
            distance = point_base.distance(point_next)
            if(distance <= self.__distance_random_move_max):
                return point_next


    class SearchingData:

        #カプセル化するデータは「探索済みデータ」および「探索済みデータの保存方法」
        #他にも、移動距離の計算方法や時間重複の排除方法などの「知識」をここに集約

        def __init__(self):
            self.__points = list()
            self.__times = list()
            self.__pollutions = list()


        def Append(self, point, time, pollution):

            self.__points.append(point)
            self.__times.append(time)
            self.__pollutions.append(pollution)


        def Print(self):
            print(self.__points)
            print(self.__times)
            print(self.__pollutions)


        def Save(self, savePath):
            """データの保存を行う関数"""

            x_save = self.__xList()
            y_save = self.__yList()



            time_save = self.__times
            pollution_save = self.__pollutions
            ####### 変更するときは自己責任でお願いします, バックアップをとっておきましょう #####################
            ### 下手に変更すると濃度ファイルから濃度値を読み取れなくなります #################################
            indexNames = ["x", "y", "time", "pollution"]
            values = [x_save, y_save, time_save, pollution_save]
            ###########################################################

            #保存にはPandasライブラリを使っています。データフレーム型という特殊な型を使っています（詳しくはWebで)
            datas = pd.DataFrame(index=[], columns=[])
            #保存するインデックス名前と値を対応づける
            for i in range(len(indexNames)):
                datalog = pd.DataFrame(index=[], columns=[])
                #単一の値（非リスト）だと保存できない。そのため、単一の値である場合はリストに変換する
                if(type(values[i]) == list):
                    datalog[indexNames[i]] = values[i]
                else: #非リストの場合
                    datalog[indexNames[i]] = [values[i]]

                datas = pd.concat([datas, datalog], axis = 1)

            #保存先は文字列型で指定する必要がある。ここれ一応文字列型に変換
            savePath = str(savePath)
            #ファイル芽、パス名から拡張子を取得
            not_used, ext = os.path.splitext(savePath)

            #拡張子によって保存用関数を選択
            if(ext == '.pkl'):
                datas.to_pickle(savePath)

            elif(ext == '.csv'):
                datas.to_csv(savePath)

            else:
                raise TypeError('pkl形式かcsv形式の保存にのみ対応しています')

        def __DataLength(self):
            #TODO ポイントの要素数と時間や濃度のリストも要素数が等しいかどうか
            return len(self.__points)

        def __xList(self):
            num_points = self.__DataLength()
            xList = list()

            for i in range(num_points):
                xList.append(self.__points[i].GetX())

            return xList

        def __yList(self):
            num_points = self.__DataLength()
            yList = list()

            for i in range(num_points):
                yList.append(self.__points[i].GetY())

            return yList




        def LastPoint(self):
            pass
            return


        def View(self, graph_object, cmap = 'binary', c = 'red', s = 5, alpha = 0.3, marker='o', norm=None, vmin=None, vmax=None, linewidths=None, edgecolors=None, data=None):
            """濃度分布の描画を行う"""
        #やたらメソッドの引数が多いですが、これはPythonの「デフォルト引数」機能を使っています（詳しくはWebで)
        #デフォルトの描画設定を、透明度(alpha) = 0.3, カラーマップをbinaryにしています。

            xList = self.__xList()
            yList = self.__yList()

            graph_object.scatter(xList, yList, cmap = cmap, c = c, s = s, alpha = alpha, marker = marker, norm = norm,\
                                  vmin = vmin, vmax = vmax, linewidths = linewidths,\
                                  edgecolors = edgecolors, data = data)

        #matplotlib、特にplt.show()は挙動が掴みづらいと思うので、調べて勉強することをおすすめします
        #plt.show()
            return graph_object #濃度分布をグラフオブジェクトに描いたあと、呼び出し元にグラフオブジェクトを返却します
