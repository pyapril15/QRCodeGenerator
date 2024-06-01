# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qrcode.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                               QLabel, QLineEdit, QMainWindow, QPushButton,
                               QSizePolicy, QSlider, QTextEdit, QVBoxLayout,
                               QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 622)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.property_frm = QFrame(self.centralwidget)
        self.property_frm.setObjectName(u"property_frm")
        self.property_frm.setFrameShape(QFrame.NoFrame)
        self.property_frm.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.property_frm)
        self.verticalLayout_8.setSpacing(5)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.input_title_frm = QFrame(self.property_frm)
        self.input_title_frm.setObjectName(u"input_title_frm")
        self.input_title_frm.setFrameShape(QFrame.NoFrame)
        self.input_title_frm.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.input_title_frm)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 2, 2, 2)
        self.input_title = QLabel(self.input_title_frm)
        self.input_title.setObjectName(u"input_title")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.input_title.setFont(font)

        self.verticalLayout.addWidget(self.input_title)

        self.input_frm = QFrame(self.input_title_frm)
        self.input_frm.setObjectName(u"input_frm")
        self.input_frm.setFrameShape(QFrame.StyledPanel)
        self.input_frm.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.input_frm)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.textEdit = QTextEdit(self.input_frm)
        self.textEdit.setObjectName(u"textEdit")

        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)

        self.verticalLayout.addWidget(self.input_frm)

        self.verticalLayout_8.addWidget(self.input_title_frm)

        self.setting_frm = QFrame(self.property_frm)
        self.setting_frm.setObjectName(u"setting_frm")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setting_frm.sizePolicy().hasHeightForWidth())
        self.setting_frm.setSizePolicy(sizePolicy)
        self.setting_frm.setFrameShape(QFrame.NoFrame)
        self.setting_frm.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.setting_frm)
        self.verticalLayout_7.setSpacing(5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(5, 2, 2, 2)
        self.setting_title = QLabel(self.setting_frm)
        self.setting_title.setObjectName(u"setting_title")
        self.setting_title.setFont(font)

        self.verticalLayout_7.addWidget(self.setting_title)

        self.version_frm = QFrame(self.setting_frm)
        self.version_frm.setObjectName(u"version_frm")
        self.version_frm.setFrameShape(QFrame.NoFrame)
        self.version_frm.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.version_frm)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.version_title = QLabel(self.version_frm)
        self.version_title.setObjectName(u"version_title")
        font1 = QFont()
        font1.setPointSize(12)
        self.version_title.setFont(font1)

        self.verticalLayout_2.addWidget(self.version_title)

        self.version_description = QLabel(self.version_frm)
        self.version_description.setObjectName(u"version_description")
        font2 = QFont()
        font2.setItalic(True)
        self.version_description.setFont(font2)

        self.verticalLayout_2.addWidget(self.version_description)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.version_slider = QSlider(self.version_frm)
        self.version_slider.setObjectName(u"version_slider")
        self.version_slider.setCursor(QCursor(Qt.PointingHandCursor))
        self.version_slider.setMinimum(1)
        self.version_slider.setMaximum(40)
        self.version_slider.setPageStep(2)
        self.version_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.version_slider)

        self.version_slider_value = QLabel(self.version_frm)
        self.version_slider_value.setObjectName(u"version_slider_value")

        self.horizontalLayout_2.addWidget(self.version_slider_value)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalLayout_7.addWidget(self.version_frm)

        self.box_size_frm = QFrame(self.setting_frm)
        self.box_size_frm.setObjectName(u"box_size_frm")
        self.box_size_frm.setFrameShape(QFrame.NoFrame)
        self.box_size_frm.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.box_size_frm)
        self.verticalLayout_3.setSpacing(8)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.box_size_title = QLabel(self.box_size_frm)
        self.box_size_title.setObjectName(u"box_size_title")
        self.box_size_title.setFont(font1)

        self.verticalLayout_3.addWidget(self.box_size_title)

        self.box_size_description = QLabel(self.box_size_frm)
        self.box_size_description.setObjectName(u"box_size_description")
        self.box_size_description.setFont(font2)

        self.verticalLayout_3.addWidget(self.box_size_description)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.box_size_slider = QSlider(self.box_size_frm)
        self.box_size_slider.setObjectName(u"box_size_slider")
        self.box_size_slider.setCursor(QCursor(Qt.PointingHandCursor))
        self.box_size_slider.setMinimum(1)
        self.box_size_slider.setMaximum(40)
        self.box_size_slider.setPageStep(2)
        self.box_size_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.box_size_slider)

        self.box_size_slider_value = QLabel(self.box_size_frm)
        self.box_size_slider_value.setObjectName(u"box_size_slider_value")

        self.horizontalLayout_3.addWidget(self.box_size_slider_value)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalLayout_7.addWidget(self.box_size_frm)

        self.border_size_frm = QFrame(self.setting_frm)
        self.border_size_frm.setObjectName(u"border_size_frm")
        self.border_size_frm.setFrameShape(QFrame.NoFrame)
        self.border_size_frm.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.border_size_frm)
        self.verticalLayout_4.setSpacing(8)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.border_size_title = QLabel(self.border_size_frm)
        self.border_size_title.setObjectName(u"border_size_title")
        self.border_size_title.setFont(font1)

        self.verticalLayout_4.addWidget(self.border_size_title)

        self.border_size_description = QLabel(self.border_size_frm)
        self.border_size_description.setObjectName(u"border_size_description")
        self.border_size_description.setFont(font2)

        self.verticalLayout_4.addWidget(self.border_size_description)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.border_size_slider = QSlider(self.border_size_frm)
        self.border_size_slider.setObjectName(u"border_size_slider")
        self.border_size_slider.setCursor(QCursor(Qt.PointingHandCursor))
        self.border_size_slider.setMinimum(1)
        self.border_size_slider.setMaximum(40)
        self.border_size_slider.setPageStep(2)
        self.border_size_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.border_size_slider)

        self.border_size_slider_value = QLabel(self.border_size_frm)
        self.border_size_slider_value.setObjectName(u"border_size_slider_value")

        self.horizontalLayout_4.addWidget(self.border_size_slider_value)

        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.verticalLayout_7.addWidget(self.border_size_frm)

        self.fill_color_frm = QFrame(self.setting_frm)
        self.fill_color_frm.setObjectName(u"fill_color_frm")
        self.fill_color_frm.setFrameShape(QFrame.NoFrame)
        self.fill_color_frm.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.fill_color_frm)
        self.verticalLayout_5.setSpacing(8)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(2, 2, 2, 2)
        self.fill_color_title = QLabel(self.fill_color_frm)
        self.fill_color_title.setObjectName(u"fill_color_title")
        self.fill_color_title.setFont(font1)

        self.verticalLayout_5.addWidget(self.fill_color_title)

        self.fill_color_description = QLabel(self.fill_color_frm)
        self.fill_color_description.setObjectName(u"fill_color_description")
        self.fill_color_description.setFont(font2)

        self.verticalLayout_5.addWidget(self.fill_color_description)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.select_fill_color = QPushButton(self.fill_color_frm)
        self.select_fill_color.setObjectName(u"select_fill_color")
        self.select_fill_color.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_5.addWidget(self.select_fill_color)

        self.fill_color_value = QLineEdit(self.fill_color_frm)
        self.fill_color_value.setObjectName(u"fill_color_value")
        self.fill_color_value.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.fill_color_value)

        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.verticalLayout_7.addWidget(self.fill_color_frm)

        self.background_color_frm = QFrame(self.setting_frm)
        self.background_color_frm.setObjectName(u"background_color_frm")
        self.background_color_frm.setFrameShape(QFrame.NoFrame)
        self.background_color_frm.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.background_color_frm)
        self.verticalLayout_6.setSpacing(8)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(2, 2, 2, 2)
        self.background_color_title = QLabel(self.background_color_frm)
        self.background_color_title.setObjectName(u"background_color_title")
        self.background_color_title.setFont(font1)

        self.verticalLayout_6.addWidget(self.background_color_title)

        self.background_color_description = QLabel(self.background_color_frm)
        self.background_color_description.setObjectName(u"background_color_description")
        self.background_color_description.setFont(font2)

        self.verticalLayout_6.addWidget(self.background_color_description)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.select_background_color = QPushButton(self.background_color_frm)
        self.select_background_color.setObjectName(u"select_background_color")
        self.select_background_color.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_6.addWidget(self.select_background_color)

        self.background_color_value = QLineEdit(self.background_color_frm)
        self.background_color_value.setObjectName(u"background_color_value")
        self.background_color_value.setReadOnly(True)

        self.horizontalLayout_6.addWidget(self.background_color_value)

        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.verticalLayout_7.addWidget(self.background_color_frm)

        self.verticalLayout_8.addWidget(self.setting_frm)

        self.horizontalLayout.addWidget(self.property_frm)

        self.output_frm = QFrame(self.centralwidget)
        self.output_frm.setObjectName(u"output_frm")
        self.output_frm.setFrameShape(QFrame.NoFrame)
        self.output_frm.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.output_frm)
        self.verticalLayout_9.setSpacing(5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(2, 2, 2, 2)
        self.result_frm = QFrame(self.output_frm)
        self.result_frm.setObjectName(u"result_frm")
        self.result_frm.setFrameShape(QFrame.StyledPanel)
        self.result_frm.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_10 = QVBoxLayout(self.result_frm)
        self.verticalLayout_10.setSpacing(5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(2, 2, 2, 2)
        self.result_qrcode = QLabel(self.result_frm)
        self.result_qrcode.setObjectName(u"result_qrcode")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.result_qrcode.sizePolicy().hasHeightForWidth())
        self.result_qrcode.setSizePolicy(sizePolicy1)
        self.result_qrcode.setMinimumSize(QSize(100, 100))
        self.result_qrcode.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.result_qrcode)

        self.verticalLayout_9.addWidget(self.result_frm)

        self.generate_qrcode = QPushButton(self.output_frm)
        self.generate_qrcode.setObjectName(u"generate_qrcode")
        self.generate_qrcode.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_9.addWidget(self.generate_qrcode)

        self.save_qrcode = QPushButton(self.output_frm)
        self.save_qrcode.setObjectName(u"save_qrcode")
        self.save_qrcode.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_9.addWidget(self.save_qrcode)

        self.horizontalLayout.addWidget(self.output_frm)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.version_slider.valueChanged.connect(self.version_slider_value.setNum)
        self.box_size_slider.valueChanged.connect(self.box_size_slider_value.setNum)
        self.border_size_slider.valueChanged.connect(self.border_size_slider_value.setNum)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QR Code Generator", None))
        self.input_title.setText(QCoreApplication.translate("MainWindow", u"Content of the QR Code", None))
        # if QT_CONFIG(tooltip)
        self.textEdit.setToolTip(QCoreApplication.translate("MainWindow", u"Enter text", None))
        # endif // QT_CONFIG(tooltip)
        self.setting_title.setText(QCoreApplication.translate("MainWindow", u"QR Code Settings", None))
        self.version_title.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.version_description.setText(
            QCoreApplication.translate("MainWindow", u"Controls the size of the QR Code", None))
        # if QT_CONFIG(tooltip)
        self.version_slider.setToolTip(QCoreApplication.translate("MainWindow", u"QR code version", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.version_slider_value.setToolTip(QCoreApplication.translate("MainWindow", u"Version value", None))
        # endif // QT_CONFIG(tooltip)
        self.version_slider_value.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.box_size_title.setText(QCoreApplication.translate("MainWindow", u"Box Size", None))
        self.box_size_description.setText(
            QCoreApplication.translate("MainWindow", u"Controls the pixel size of each box", None))
        # if QT_CONFIG(tooltip)
        self.box_size_slider.setToolTip(QCoreApplication.translate("MainWindow", u"QR Code box size", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.box_size_slider_value.setToolTip(QCoreApplication.translate("MainWindow", u"Box size value", None))
        # endif // QT_CONFIG(tooltip)
        self.box_size_slider_value.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.border_size_title.setText(QCoreApplication.translate("MainWindow", u"Border Size", None))
        self.border_size_description.setText(
            QCoreApplication.translate("MainWindow", u"Controls the border size of the QR Code", None))
        # if QT_CONFIG(tooltip)
        self.border_size_slider.setToolTip(QCoreApplication.translate("MainWindow", u"QR Code border size", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.border_size_slider_value.setToolTip(QCoreApplication.translate("MainWindow", u"Border size value", None))
        # endif // QT_CONFIG(tooltip)
        self.border_size_slider_value.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.fill_color_title.setText(QCoreApplication.translate("MainWindow", u"Fill Color", None))
        self.fill_color_description.setText(
            QCoreApplication.translate("MainWindow", u"Select the fill color for the QR Code", None))
        # if QT_CONFIG(tooltip)
        self.select_fill_color.setToolTip(QCoreApplication.translate("MainWindow", u"QR Code color", None))
        # endif // QT_CONFIG(tooltip)
        self.select_fill_color.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        self.background_color_title.setText(QCoreApplication.translate("MainWindow", u"Background Color", None))
        self.background_color_description.setText(
            QCoreApplication.translate("MainWindow", u"Select the background color for the QR Code", None))
        # if QT_CONFIG(tooltip)
        self.select_background_color.setToolTip(
            QCoreApplication.translate("MainWindow", u"QR Code background color", None))
        # endif // QT_CONFIG(tooltip)
        self.select_background_color.setText(QCoreApplication.translate("MainWindow", u"Select Color", None))
        # if QT_CONFIG(tooltip)
        self.result_qrcode.setToolTip(QCoreApplication.translate("MainWindow", u"QR Code", None))
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.generate_qrcode.setToolTip(QCoreApplication.translate("MainWindow", u"Generate QR Code", None))
        # endif // QT_CONFIG(tooltip)
        self.generate_qrcode.setText(QCoreApplication.translate("MainWindow", u"Generate QR Code", None))
        # if QT_CONFIG(tooltip)
        self.save_qrcode.setToolTip(QCoreApplication.translate("MainWindow", u"Save QR Code", None))
        # endif // QT_CONFIG(tooltip)
        self.save_qrcode.setText(QCoreApplication.translate("MainWindow", u"Save QR Code", None))
    # retranslateUi
