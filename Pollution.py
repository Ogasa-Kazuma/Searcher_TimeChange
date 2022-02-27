# -*- coding: utf-8 -*-
import glob
import pandas as pd
import math
import re
import importlib
from PointClass import Point

class Pollution:

    #コンストラクタに入れるものが実装詳細となるものが多い
    def __init__(self, pollutionFileDirectory, format, fileReader):
        self.__pollutionFileDirectory = pollutionFileDirectory
        self.__format = format
        self.__fileReader = fileReader

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



    def StraightLine(self, point_start, point_last, time_start, speed):


        #2点間の角度計算
        #x座標、y座標の集合をtimeにまとめたクラスにする？

        #メソッドをクラスやメソッド内メソッドにまとめたほうがわかりやすい！
        x, y = self.__CalcPointsOnLine(point_start, point_last)

        x, y = self.__RoundPoints(x, y)
        x, y = self.__DeleteDupl(x, y)
        x, y = self.__ToInt(x, y)

        t = self.__TimeList(point_start, x, y, time_start, speed)


        pollutions = self.__Pollutions(x, y, t)

        pointsAndPollutions = self.__ConvertPointsAndPollutionsToOneList(x, y, t, pollutions)

        return self.PollutionStraightLine(pointsAndPollutions)



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

            if(self.__counter > len(self.__pointAndPollutions)):
                self.__counter = 0
                return []

            self.__counter += 1
            return self.__pointAndPollutions
