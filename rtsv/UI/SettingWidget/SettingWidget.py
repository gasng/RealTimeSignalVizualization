from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QFileDialog

from rtsv.UI.SettingWidget.SettingWidget_ui import Ui_SettingWidget

DIR_PATH = 'C://Users/Elizaveta/station_data/L000100/'


class SettingWidget(QWidget):
    closed = Signal()
    def __init__(self):
        super(SettingWidget, self).__init__()
        self.dir_path = DIR_PATH

        self.ui = Ui_SettingWidget()
        self.ui.setupUi(self)
        self.time_lag = self.ui.TimeLagSB.value()
        self.__update_line()

        self.__create_callbacks()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def __create_callbacks(self):
        self.ui.SettingGB.toggled.connect(self.__update_group_box)
        self.ui.TimeLagSB.valueChanged.connect(self.__update_time_lag)
        self.ui.ChooseDirBtn.clicked.connect(self.__choose_dir)

    def __update_time_lag(self):
        self.time_lag = self.ui.TimeLagSB.value()

    def __update_group_box(self):
        check = self.ui.SettingGB.isChecked()
        if check:
            self.ui.label.setEnabled(True)
            self.ui.TimeLagSB.setEnabled(True)
        else:
            self.ui.label.setEnabled(False)
            self.ui.TimeLagSB.setEnabled(False)

    def __choose_dir(self):
        self.dir_path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Выберите директорию",
        )
        self.__update_line()

    def __update_line(self):
        self.ui.PathLineEdit.setText(self.dir_path)
