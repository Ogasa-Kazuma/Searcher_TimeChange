
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

import Random_Move_Searcher
importlib.reload(Random_Move_Searcher)
#----------------------------------------------------

#--------------　メッセージ ----------------------
#データを直で触らせない
#pollutionクラスやpointクラスにメソッドがまとまってるおかげで、探索者クラスのコードが少なく済む！
#内部クラスの利点は、親クラスに直接触れずに親クラスの拡張？ができること！
#


class Speed:

    def __init__(self, base_unit_compare_meter):
        self.__compare_meter = 1

    def CalcTime(point_start, point_last):
        pass


class TimeRange:

    def __init__(self, time_start, time_last):
        self.__time_start = time_start
        self.__time_last = time_last

    def __Time_Last(self):
        return self.__time_last

    def IsTimeOver(self, time):
        if(time > self.__Time_Last()):
            return True

        return False


    def __Time_Start(self):
        return self.__time_start

    def GetStartTime(self):
        return self.__Time_Start()























#-------------------------------------------------------------------
def main():


    pklReader = Pickle_Reader.PickleReader()
    pollutionDataReader = PollutionDataReader("PollutionFiles/", '.pkl', pklReader)
    print(pollutionDataReader.IsInRange(Point(0, 0)))
    point_random = pollutionDataReader.RandomPoint()
    point_random.Print()


    randomMoveSearcher = Random_Move_Searcher.RandomMoveSearcher(pollutionDataReader, randomMoveScope = 30, speed = 2)
    searchingData = randomMoveSearcher.TargetPollutionValueOverPoint(point_start = Point(0, 0), time_range = TimeRange(0, 50), targetPollutionValue = 100)
    #ぐちゃぐちゃしたものをsearchingDataオブジェクト、クラスの中で完結させて簡潔させてるから
    #呼び出し手はスッキリとしたコードになる！
    searchingData.Print()
    searchingData.Save("unko.csv")
    fig = plt.figure()
    graph_object = fig.add_subplot(111)
    #pollutionDataReader.View(graph_object, time = 100)
    searchingData.View(graph_object, c = 'blue', s = 10)






if __name__ == "__main__":
    main()
