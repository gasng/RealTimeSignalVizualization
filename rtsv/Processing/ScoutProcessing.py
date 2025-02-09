import glob
import os

import numpy as np

from rtsv.Processing.Convertor import ScoutConvertor


class ScoutProcessing:
    @staticmethod
    def get_filenames(dir_path, number_of_channels):
        newest_folder = os.path.join(os.path.normpath(max([x[0] for x in os.walk(dir_path)], key=os.path.getmtime)),
                                     '*')
        list_of_files = glob.glob(newest_folder)
        latest_file = max(list_of_files, key=os.path.getctime)
        filename = latest_file[:latest_file.rfind('_')]
        filenames = [filename + '_{i}.dat'.format(i=i + 1) for i in range(number_of_channels)]
        condition = all([os.path.isfile(filenames[i]) for i in range(len(filenames))])
        if condition:
            return filenames
        else:
            return ScoutProcessing.get_filenames(dir_path, number_of_channels)

    @staticmethod
    def get_scout_list(files_path):
        cls_list = [ScoutConvertor.read_scout_file(*os.path.split(files_path[i]))
                    for i in range(len(files_path))]
        return cls_list

    @staticmethod
    def parse_scout(scout_list):
        cls = scout_list[0]
        dt = np.round(cls.quantum_time, decimals=4)
        length = len(cls.data)
        return dt, length

    @staticmethod
    def get_data(scout_list):
        data_list = [cls.data for cls in scout_list]
        data = np.array(data_list).T
        return data