
import importlib
import matplotlib.pyplot as plt
import PointClass
importlib.reload(PointClass)
from PointClass import Point



import Pollution
importlib.reload(Pollution)
from Pollution import Pollution

import Pickle_Reader


def AnimatePollutionTimeChange(pollution, time_start, time_last, step):
#pollutionが実装の詳細（View）を隠してるおかげでカプセル化が保たれてる
    for t_i in range(time_start, time_last, step):
        fig = plt.figure()
        graph = fig.add_subplot(111)
        print(t_i)
        pollution.View(graph, time = t_i)




def main():

    pollutionFileReader = Pickle_Reader.PickleReader()
    pollution = Pollution("PollutionFiles/", '.pkl', pollutionFileReader)
    stragihtLine = pollution.StraightLine(Point(0, 0), Point(5, 5), time_start = 10, speed = 2)
    stragihtLine.Print()

    for x_i, y_i, t_i, pollution_i in stragihtLine.Next():
        print("line")
        print(x_i)
        print(y_i)
        print(t_i)
        print(pollution_i)




    print(pollutionFileReader.Read("PollutionFiles/0.pkl"))

    AnimatePollutionTimeChange(pollution, time_start = 0, time_last = 50, step = 1)













if __name__ == "__main__":
    main()
