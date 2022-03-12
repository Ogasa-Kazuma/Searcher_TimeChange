# -*- coding: utf-8 -*-
import glob

import pandas as pd
import random
import math
import re
import copy
import importlib
from PointClass import Point

class PollutionDataReader:
    """ファイルから濃度値を取得するクラス"""

    #コンストラクタ
    def __init__(self, pollutionFileDirectory, format, fileReader):
        self.__pollutionFileDirectory = pollutionFileDirectory
        self.__format = format
        self.__fileReader = fileReader


#--------------- パブリックメソッド ----------------------------
#
# パブリックメソッドはクラス外からもアクセスできます
#
#-------------------------------------------------------------



    def GetPollution(self, x, y, t):
        """指定した座標および時間の濃度値を取得する"""
        pollution = self.__Read(x, y, t)
        return pollution

    def IsInRange(self, point):

        file = self.__pollutionFileDirectory + str(0) + self.__format
        file = self.__fileReader.Read(file)


        xlim = int(file['x'][0]) - 1
        ylim = int(file['y'][0]) - 1


        isUnderZero = point.IsUnderX(0) or point.IsUnderY(0)
        isOverLimit = point.IsOverX(xlim) or point.IsOverY(ylim)

        if(isUnderZero or isOverLimit):
            return False


        return True



    def RandomPoint(self):

        file = self.__OpenFile(time = 0)
        xIndex = self.__xIndexName()
        yIndex = self.__yIndexName()

        xlim = file[xIndex][0] - 1
        ylim = file[yIndex][0] - 1


        while(1):


            x_random = random.randint(-xlim, xlim + 1)
            y_random = random.randint(-ylim, ylim + 1)

            point_random = Point(x_random, y_random)
            if(self.IsInRange(point_random)):
                return point_random





    def View(self, graph_object, time, cmap = 'binary', alpha = 0.3, marker='o', norm=None, vmin=None, vmax=None, linewidths=None, verts=None, edgecolors=None, hold=None, data=None):
        """指定した時間での濃度分布モデルを描画する"""

        #濃度値ファイルの読み出し
        path = self.__pollutionFileDirectory + str(time)  + self.__format
        pollutionLog = self.__fileReader.Read(path)



        #-------------- 変更しないでください ---------------
        xlim = int(pollutionLog["x"][0])
        ylim = int(pollutionLog["y"][0])
        #---------------------------------------------

        new_x = list()
        new_y = list()

        #表示できる形式に、座標データを変換
        for x_i in range(0, xlim, 1):
            for y_i in range(0, ylim, 1):

                new_x.append(x_i)
                new_y.append(y_i)

        #表示できるように、濃度値データのデータ構造と値を調整
        plns = copy.deepcopy(pollutionLog["pollutions"])
        plns = plns.values.tolist()
        maxPln = max(plns)
        for i in range(len(plns)):
            plns[i] = plns[i] / maxPln


        #散布図を描画
        graph_object.scatter(new_x, new_y, c = plns, cmap = cmap, alpha = alpha, marker = marker, norm = norm,\
                              vmin = vmin, vmax = vmax, linewidths = linewidths,\
                              edgecolors = edgecolors, data = data)

        #グラフオブジェクトを返却
        return graph_object


    def StraightLine(self, point_start, point_last, time_start, speed):
        """指定した2点間の座標、濃度値、かかる時間を計算し、まとめて返す"""

        #2点間に存在する座標を計算
        x, y = self.__CalcPointsOnLine(point_start, point_last)

        #2点間座標を整数に変換したり、重複を排除する
        x, y = self.__RoundPoints(x, y)
        x, y = self.__DeleteDupl(x, y)
        x, y = self.__ToInt(x, y)


        #上記で計算した座標について、その地点にたどりつくまでの時間を各点について計算
        t = self.__TimeList(point_start, x, y, time_start, speed)

        #各点および時間での濃度値を計算
        pollutions = self.__Pollutions(x, y, t)


        #濃度値と座標を直線オブジェクトとして返却
        pointsAndPollutions = self.__ConvertPointsAndPollutionsToOneList(x, y, t, pollutions)
        print(pointsAndPollutions)
        return self.PollutionStraightLine(pointsAndPollutions)


#-------------- パブリックメソッド -------------------------------------




#-------------　プライベートメソッド ------------------------------------
#
# プライベートメソッドはクラス外からアクセスできません
#
#----------------------------------------------------------------------

    def __xIndexName(self):
        return "x"

    def __yIndexName(self):
        return "y"

    def __pollutionIndexName(self):
        return "pollutions"






    def __Read(self, x, y, t):

        #切り上げ、切り捨て
        t_down = self.__RoundDown(t)
        t_up = self.__RoundUp(t)

        file_down = self.__SpecifyFile(t_down)
        file_up = self.__SpecifyFile(t_up)

        pollution_down = self.__ReadPollution(file_down, x, y)
        pollution_up = self.__ReadPollution(file_up, x, y)

        #線形補完
        pollution = self.__LinearInterpolation(t, pollution_down, pollution_up, t_down, t_up)

        return pollution


    def __RemoveExpectAlphabet(self, string):
        string = self.__ToString(string)
        string = re.sub(r"[^a-zA-Z]", "", string)
        return string



    def __ToString(self, string):
        return str(string)


    def __RoundUp(self, value):
        value = math.ceil(value)
        return value

    def __RoundDown(self, value):
        value = math.floor(value)
        return value


    def __OpenFile(self, time):
        fileLocation = self.__pollutionFileDirectory + str(time) + self.__format
        file = self.__fileReader.Read(fileLocation)
        return file


    def __SpecifyFile(self, t):
        fileLocation = self.__pollutionFileDirectory + str(t) + self.__format
        files = glob.glob(fileLocation, recursive=True)
        file = files[0]
        return file



    def __ReadPollution(self, path, x, y):

        file = self.__fileReader.Read(path)

        count = file['y'][0] * x + y
        concent = file['pollutions'][count]

        return concent


    def __LinearInterpolation(self, t, pollution_down, pollution_up, t_down, t_up):

        diff_pollution = pollution_up - pollution_down
        diff_t = t_up - t_down

        #整数値の時間が入力されたら線形補完の必要なし
        if(not diff_t):
            return pollution_down

        #濃度変化と時間の変化割合
        ratio = diff_pollution / diff_t

        #tの小数点部分のみ計算
        t_offset = t - t_down

        pollution_change = ratio * t_offset
        pollution = pollution_down + pollution_change

        return pollution






    def __CalcPointsOnLine(self, point_start, point_last):


        angle = point_start.Degrees(point_last)

        distance = point_start.distance(point_last)

        x = list()
        y = list()


        for i in range(0, round(distance * 10), 1):

            dis_i = i * 0.1
            start_x = point_start.GetX()
            start_y = point_start.GetY()

            x.append(start_x + dis_i * math.cos(math.radians(angle)))
            y.append(start_y + dis_i * math.sin(math.radians(angle)))




        return x, y


    def __RoundPoints(self, xList, yList):

        xList = list(map(round, xList))
        yList = list(map(round, yList))

        return xList, yList


    def __DeleteDupl(self, xList, yList):

        new_x = list()
        new_y = list()

        for i in range(len(xList)):
            if(not(xList[i] in new_x and yList[i] in new_y)):
                new_x.append(xList[i])
                new_y.append(yList[i])


        return new_x, new_y


    def __ToInt(self, xList, yList):

        xList = list(map(int, xList))
        yList = list(map(int, yList))



        return xList, yList



    def __TimeList(self, point_start, x, y, time_start, speed):

        tList = list()
        element_count_xy = len(x)
        for i in range(element_count_xy):
                time = point_start.time(Point(x[i], y[i]), speed)
                time = time + time_start
                tList.append(time)

        return tList


    def __Pollutions(self, x, y, t):
        pollution_collection = list()
        for i in range(len(x)):
            pollution = self.__Read(x[i], y[i], t[i])
            pollution_collection.append(pollution)

        return pollution_collection


    def __ConvertPointsAndPollutionsToOneList(self, x, y, t, pollutions):
        pointsAndPollutions = list()
        numElements = len(pollutions)
        for i in range(numElements):
            pointsAndPollutions.append([x[i], y[i], t[i], pollutions[i]])

        return pointsAndPollutions




################################################################
    class PollutionStraightLine:


        def __init__(self, pointsAndPollutions):
            self.__pointAndPollutions = pointsAndPollutions
            self.__counter = 0

        def Print(self):
            print(self.__pointAndPollutions)

        def Next(self):

            if(self.__counter >= len(self.__pointAndPollutions)):
                self.__counter = 0
                return []


            x = self.__pointAndPollutions[self.__counter][0]
            y = self.__pointAndPollutions[self.__counter][1]
            t = self.__pointAndPollutions[self.__counter][2]
            pollution = self.__pointAndPollutions[self.__counter][3]

            self.__counter += 1

            return Point(x, y), t, pollution

        def HasNext(self):
            hasNext = (not (self.__counter >= len(self.__pointAndPollutions)))
            return hasNext




        def __PointAndPollutions(self):
            return self.__pointAndPollutions

        def __DataLength(self):
            return len(self.__PointAndPollutions())
