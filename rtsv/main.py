import os
import sys

import numpy as np
import pyqtgraph as pg
from PySide6 import QtWidgets, QtCore

from rtsv.Processing.ScoutProcessing import ScoutProcessing
from rtsv.UI.PlotWidget.PlotWidget import PlotWidget
from rtsv.UI.SettingWidget.SettingWidget import SettingWidget
from rtsv.UI.Worker import SignalReader

T = 3600
TIME_MULTIPLIER = 1000

class SignalVisualizer(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.checker = 0
        self.plot_time = 5
        self.start_saving = self.plot_time
        self.reader_thread = None
        self.ax_1_widget = None
        self.ax_2_widget = None
        self.ax_3_widget = None
        self.timer = None

        self.setting_widget = SettingWidget()
        self.plot_widget = PlotWidget()
        self.setting_widget.show()
        self.__create_callbacks()
    #     self.__set_theme()
    #
    # def __set_theme(self):
    #     sshFile = "./rtsv/UI/Themes/DarkTheme.stylesheet"
    #     if getattr(sys, 'frozen', False):
    #         sshFile = os.path.join(sys._MEIPASS, sshFile)
    #
    #     with open(sshFile, "r") as fh:
    #         # self.setting_widget.setStyleSheet(fh.read())
    #         self.plot_widget.setStyleSheet(fh.read())

    def __create_callbacks(self):
        self.setting_widget.ui.StartBtn.clicked.connect(self.__start)
        self.plot_widget.ui.StopBtn.clicked.connect(self.__stop)
        self.plot_widget.closed.connect(self.__stop)
        self.setting_widget.closed.connect(self.__close_app)

    def __start(self):
        self.time_lag = self.setting_widget.time_lag
        self.setting_widget.hide()
        self.plot_widget.show()

        self.reader_thread = SignalReader(self.setting_widget.dir_path)
        self.reader_thread.new_data.connect(self.__update_data)
        self.reader_thread.start()

        self.__create_plot_widget()

    def __create_plot_widget(self):
        # self.plot_widget.ui.PlotLayout.setParent(None)
        figure_widget = QtWidgets.QWidget()
        vlayout = QtWidgets.QVBoxLayout()

        self.ax_1_widget = pg.PlotWidget()
        # self.ax_1_widget.setBackground('w')
        self.ax_1_widget.getPlotItem().hideAxis('bottom')
        self.ax_1_widget.getPlotItem().hideAxis('left')

        self.ax_2_widget = pg.PlotWidget()
        # self.ax_2_widget.setBackground('w')
        self.ax_2_widget.getPlotItem().hideAxis('bottom')
        self.ax_2_widget.getPlotItem().hideAxis('left')

        self.ax_3_widget = pg.PlotWidget()
        # self.ax_3_widget.setBackground('w')
        self.ax_3_widget.getPlotItem().hideAxis('bottom')
        self.ax_3_widget.getPlotItem().hideAxis('left')

        vlayout.addWidget(self.ax_1_widget)
        vlayout.addWidget(self.ax_2_widget)
        vlayout.addWidget(self.ax_3_widget)
        figure_widget.setLayout(vlayout)
        self.plot_widget.ui.PlotLayout.addWidget(figure_widget)
        self.__create_hour_data()

    def __create_hour_data(self):
        self.old_filenames = ScoutProcessing.get_filenames(self.setting_widget.dir_path, 3)
        scout_list = ScoutProcessing.get_scout_list(self.old_filenames)

        self.dt, self.length = ScoutProcessing.parse_scout(scout_list)
        data_size = T * self.length
        self.hour_data = np.zeros((data_size, 3))
        self.file_time_length = int(self.dt * self.length)
        data = ScoutProcessing.get_data(scout_list)
        self.start_saving = self.plot_time + self.time_lag * self.file_time_length
        self.hour_data[self.start_saving * self.length: (self.start_saving +  self.file_time_length) * self.length, :] = data

        self.start = 0
        self.end = self.plot_time * self.length
        self.y = self.hour_data[self.start: self.end, :]
        self.x = list(np.arange(self.y.shape[0]) * self.dt)

        # pen = pg.mkPen(color=(0, 0, 255))
        self.ax_1 = self.ax_1_widget.plot(x=self.x, y=self.y[:, 0], pen=pg.mkPen(color=(0, 0, 255)))
        self.ax_2 = self.ax_2_widget.plot(x=self.x, y=self.y[:, 1], pen=pg.mkPen(color=(0, 255, 0)))
        self.ax_3 = self.ax_3_widget.plot(x=self.x, y=self.y[:, 2], pen=pg.mkPen(color=(255, 0, 0)))

        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.dt * TIME_MULTIPLIER)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        # print('Нужное время: {time_1}; Истинное время: {time_2}'.format(time_1=self.start_saving,
        #                                                                 time_2=int(self.x[-1])),
        #       end='\r')
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + self.dt)  # Add a new value 1 higher than the last.

        self.start += 1
        self.end += 1

        self.y = self.hour_data[self.start: self.end, :]

        self.ax_1.setData(self.x, self.y[:, 0])
        self.ax_2.setData(self.x, self.y[:, 1])
        self.ax_3.setData(self.x, self.y[:, 2])

    def __update_data(self, data):
        self.start_saving += self.file_time_length
        self.hour_data[(self.start_saving - self.file_time_length) * self.length: self.start_saving * self.length, :] = data

    def __stop(self):
        if self.reader_thread:
            self.reader_thread.stop()
            self.reader_thread = None
        for i in reversed(range(self.plot_widget.ui.PlotLayout.count())):
            self.plot_widget.ui.PlotLayout.itemAt(i).widget().setParent(None)
        self.timer.stop()
        self.plot_widget.hide()
        self.setting_widget.show()

    def __close_app(self):
        if self.reader_thread:
            self.reader_thread.stop()
            self.reader_thread = None
        for i in reversed(range(self.plot_widget.ui.PlotLayout.count())):
            self.plot_widget.ui.PlotLayout.itemAt(i).widget().setParent(None)
        if self.timer:
            self.timer.stop()
        if self.ax_1_widget:
            self.ax_1_widget = None
            self.ax_2_widget = None
            self.ax_3_widget = None



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = SignalVisualizer()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
