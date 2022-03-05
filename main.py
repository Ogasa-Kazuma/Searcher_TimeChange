
import importlib
import matplotlib.pyplot as plt
import PointClass
importlib.reload(PointClass)
from PointClass import Point



import Pollution_Data_Reader
importlib.reload(Pollution_Data_Reader)
from Pollution_Data_Reader import PollutionDataReader

import Pickle_Reader


def AnimatePollutionTimeChange(pollution, time_start, time_last, step):

    for t_i in range(time_start, time_last, step):
        fig = plt.figure()
        graph = fig.add_subplot(111)
        graph = pollution.View(graph, time = t_i)





def main():

    pklReader = Pickle_Reader.PickleReader()
    pollutionDataReader = PollutionDataReader("PollutionFiles/", '.pkl', pklReader)
    print(pollutionDataReader.GetPollution(x = 0, y = 0, t = 50))


    AnimatePollutionTimeChange(pollutionDataReader, time_start = 0, time_last = 50, step = 1)













if __name__ == "__main__":
    main()
