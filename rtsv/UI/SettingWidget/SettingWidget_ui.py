# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingWidget_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_SettingWidget(object):
    def setupUi(self, SettingWidget):
        if not SettingWidget.objectName():
            SettingWidget.setObjectName(u"SettingWidget")
        SettingWidget.resize(450, 194)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingWidget.sizePolicy().hasHeightForWidth())
        SettingWidget.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(SettingWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.PathGB = QGroupBox(SettingWidget)
        self.PathGB.setObjectName(u"PathGB")
        self.horizontalLayout = QHBoxLayout(self.PathGB)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.PathLineEdit = QLineEdit(self.PathGB)
        self.PathLineEdit.setObjectName(u"PathLineEdit")

        self.horizontalLayout.addWidget(self.PathLineEdit)

        self.ChooseDirBtn = QPushButton(self.PathGB)
        self.ChooseDirBtn.setObjectName(u"ChooseDirBtn")

        self.horizontalLayout.addWidget(self.ChooseDirBtn)


        self.verticalLayout_2.addWidget(self.PathGB)

        self.SettingGB = QGroupBox(SettingWidget)
        self.SettingGB.setObjectName(u"SettingGB")
        sizePolicy.setHeightForWidth(self.SettingGB.sizePolicy().hasHeightForWidth())
        self.SettingGB.setSizePolicy(sizePolicy)
        self.SettingGB.setCheckable(True)
        self.SettingGB.setChecked(False)
        self.horizontalLayout_2 = QHBoxLayout(self.SettingGB)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.SettingGB)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.TimeLagSB = QSpinBox(self.SettingGB)
        self.TimeLagSB.setObjectName(u"TimeLagSB")
        self.TimeLagSB.setMinimum(1)
        self.TimeLagSB.setMaximum(5)
        self.TimeLagSB.setValue(2)

        self.horizontalLayout_2.addWidget(self.TimeLagSB)


        self.verticalLayout_2.addWidget(self.SettingGB)

        self.StartBtn = QPushButton(SettingWidget)
        self.StartBtn.setObjectName(u"StartBtn")

        self.verticalLayout_2.addWidget(self.StartBtn)


        self.retranslateUi(SettingWidget)

        QMetaObject.connectSlotsByName(SettingWidget)
    # setupUi

    def retranslateUi(self, SettingWidget):
        SettingWidget.setWindowTitle(QCoreApplication.translate("SettingWidget", u"RealTimeSignalVizualization", None))
        self.PathGB.setTitle(QCoreApplication.translate("SettingWidget", u"\u0412\u044b\u0431\u043e\u0440 \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440\u0438\u0438", None))
        self.ChooseDirBtn.setText(QCoreApplication.translate("SettingWidget", u"\u0412\u044b\u0431\u043e\u0440", None))
        self.SettingGB.setTitle(QCoreApplication.translate("SettingWidget", u"\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.label.setText(QCoreApplication.translate("SettingWidget", u"\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439 \u043b\u0430\u0433", None))
        self.StartBtn.setText(QCoreApplication.translate("SettingWidget", u"\u0417\u0430\u043f\u0443\u0441\u043a", None))
    # retranslateUi

