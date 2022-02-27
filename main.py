
import importlib
import PointClass
importlib.reload(PointClass)
from PointClass import Point



import Pollution
importlib.reload(Pollution)
from Pollution import Pollution







import Pickle_Reader


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


    










if __name__ == "__main__":
    main()
