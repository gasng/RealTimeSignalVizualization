from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from rtsv.UI.PlotWidget.PlotWidget_ui import Ui_PlotWidget


class PlotWidget(QWidget):
    closed = Signal()
    def __init__(self):
        super(PlotWidget, self).__init__()

        self.ui = Ui_PlotWidget()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
