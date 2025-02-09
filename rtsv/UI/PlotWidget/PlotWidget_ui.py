# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PlotWidget_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_PlotWidget(object):
    def setupUi(self, PlotWidget):
        if not PlotWidget.objectName():
            PlotWidget.setObjectName(u"PlotWidget")
        PlotWidget.resize(746, 544)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PlotWidget.sizePolicy().hasHeightForWidth())
        PlotWidget.setSizePolicy(sizePolicy)
        PlotWidget.setMinimumSize(QSize(746, 544))
        self.verticalLayout_2 = QVBoxLayout(PlotWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.PlotLayout = QVBoxLayout()
        self.PlotLayout.setObjectName(u"PlotLayout")

        self.verticalLayout_2.addLayout(self.PlotLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.StopFrame = QFrame(PlotWidget)
        self.StopFrame.setObjectName(u"StopFrame")
        self.StopFrame.setMaximumSize(QSize(16777215, 52))
        self.StopFrame.setFrameShape(QFrame.StyledPanel)
        self.StopFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.StopFrame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(597, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.StopBtn = QPushButton(self.StopFrame)
        self.StopBtn.setObjectName(u"StopBtn")

        self.horizontalLayout.addWidget(self.StopBtn)


        self.verticalLayout_2.addWidget(self.StopFrame)


        self.retranslateUi(PlotWidget)

        QMetaObject.connectSlotsByName(PlotWidget)
    # setupUi

    def retranslateUi(self, PlotWidget):
        PlotWidget.setWindowTitle(QCoreApplication.translate("PlotWidget", u"RealTimeSignalVizualization", None))
        self.StopBtn.setText(QCoreApplication.translate("PlotWidget", u"\u0421\u0442\u043e\u043f", None))
    # retranslateUi

