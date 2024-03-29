# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(803, 515)
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 371, 461))
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.Settings = QtWidgets.QWidget()
        self.Settings.setObjectName("Settings")
        self.frame = QtWidgets.QFrame(self.Settings)
        self.frame.setGeometry(QtCore.QRect(0, 10, 311, 381))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 282, 140))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.SampleFreq = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.SampleFreq.setFont(font)
        self.SampleFreq.setObjectName("SampleFreq")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.SampleFreq)
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.SampleNo = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.SampleNo.setFont(font)
        self.SampleNo.setObjectName("SampleNo")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.SampleNo)
        self.verticalLayout_3.addLayout(self.formLayout_3)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 130, 218, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.Vcoil = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Vcoil.setFont(font)
        self.Vcoil.setObjectName("Vcoil")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Vcoil)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.Fcoil = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Fcoil.setFont(font)
        self.Fcoil.setObjectName("Fcoil")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Fcoil)
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 260, 222, 121))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.Vsensor = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Vsensor.setFont(font)
        self.Vsensor.setObjectName("Vsensor")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Vsensor)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.Fsensor = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Fsensor.setFont(font)
        self.Fsensor.setObjectName("Fsensor")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Fsensor)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.tabWidget.addTab(self.Settings, "")
        self.Motorchecks = QtWidgets.QWidget()
        self.Motorchecks.setObjectName("Motorchecks")
        self.pushButton = QtWidgets.QPushButton(self.Motorchecks)
        self.pushButton.setGeometry(QtCore.QRect(50, 40, 231, 51))
        self.pushButton.setObjectName("pushButton")
        self.label_10 = QtWidgets.QLabel(self.Motorchecks)
        self.label_10.setGeometry(QtCore.QRect(50, 0, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_10.setFont(font)
        self.label_10.setAutoFillBackground(False)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_20 = QtWidgets.QLabel(self.Motorchecks)
        self.label_20.setGeometry(QtCore.QRect(40, 130, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_20.setFont(font)
        self.label_20.setAutoFillBackground(False)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.widget = QtWidgets.QWidget(self.Motorchecks)
        self.widget.setGeometry(QtCore.QRect(50, 180, 211, 171))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_21 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_21.setFont(font)
        self.label_21.setAutoFillBackground(False)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.verticalLayout_7.addWidget(self.label_21)
        self.label_22 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_22.setFont(font)
        self.label_22.setAutoFillBackground(False)
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.verticalLayout_7.addWidget(self.label_22)
        self.label_23 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label_23.setFont(font)
        self.label_23.setAutoFillBackground(False)
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.verticalLayout_7.addWidget(self.label_23)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.M1 = QtWidgets.QLCDNumber(self.widget)
        palette = QtGui.QPalette()
        self.M1.setPalette(palette)
        self.M1.setObjectName("M1")
        self.verticalLayout_8.addWidget(self.M1)
        self.M2 = QtWidgets.QLCDNumber(self.widget)
        
        self.M2.setPalette(palette)
        self.M2.setObjectName("M2")
        self.verticalLayout_8.addWidget(self.M2)
        self.M3 = QtWidgets.QLCDNumber(self.widget)
        
        self.M3.setPalette(palette)
        self.M3.setObjectName("M3")
        self.verticalLayout_8.addWidget(self.M3)
        self.horizontalLayout.addLayout(self.verticalLayout_8)
        self.tabWidget.addTab(self.Motorchecks, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.widget1 = QtWidgets.QWidget(self.tab)
        self.widget1.setGeometry(QtCore.QRect(10, 20, 359, 261))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_24 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.verticalLayout_9.addWidget(self.label_24)
        self.Scanimage = QtWidgets.QPushButton(self.widget1)
        self.Scanimage.setObjectName("Scanimage")
        self.verticalLayout_9.addWidget(self.Scanimage)
        self.label_26 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.verticalLayout_9.addWidget(self.label_26)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_9.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_9.addWidget(self.pushButton_3)
        self.label_25 = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.verticalLayout_9.addWidget(self.label_25)
        self.imageonly = QtWidgets.QPushButton(self.widget1)
        self.imageonly.setObjectName("imageonly")
        self.verticalLayout_9.addWidget(self.imageonly)
        self.tabWidget.addTab(self.tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuRun = QtWidgets.QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSystem_Checks = QtWidgets.QAction(MainWindow)
        self.actionSystem_Checks.setObjectName("actionSystem_Checks")
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionSystem_Checks)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_7.setText(_translate("MainWindow", "PicoScope "))
        self.label_8.setText(_translate("MainWindow", "Sample Frequency (Hz)"))
        self.label_9.setText(_translate("MainWindow", "Number of Samples"))
        self.label.setText(_translate("MainWindow", "Coil "))
        self.label_3.setText(_translate("MainWindow", "Voltage (Vrms)"))
        self.label_4.setText(_translate("MainWindow", "Frequency (Hz)"))
        self.label_2.setText(_translate("MainWindow", "Sensor "))
        self.label_5.setText(_translate("MainWindow", "Voltage (Vrms)"))
        self.label_6.setText(_translate("MainWindow", "Frequency (Hz)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Settings), _translate("MainWindow", "Scan options"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.label_10.setText(_translate("MainWindow", "To Check Motors press below"))
        self.label_20.setText(_translate("MainWindow", "Status:"))
        self.label_21.setText(_translate("MainWindow", "Motor 1:"))
        self.label_22.setText(_translate("MainWindow", "Motor 2:"))
        self.label_23.setText(_translate("MainWindow", "Motor 3:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Motorchecks), _translate("MainWindow", "Motor checks"))
        self.label_24.setText(_translate("MainWindow", "To take new scan and create reconstruction:"))
        self.Scanimage.setText(_translate("MainWindow", "Mode 1 "))
        self.label_26.setText(_translate("MainWindow", "If a new scan is selected choose one of the following options:"))
        self.pushButton_2.setText(_translate("MainWindow", "Fast-Scan (Low resolution)"))
        self.pushButton_3.setText(_translate("MainWindow", "Slow Scan (High resolution)"))
        self.label_25.setText(_translate("MainWindow", "To process pre-captured data:"))
        self.imageonly.setText(_translate("MainWindow", "Mode 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Mode"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuView.setTitle(_translate("MainWindow", "View "))
        self.menuRun.setTitle(_translate("MainWindow", "Run"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSystem_Checks.setText(_translate("MainWindow", "System Checks"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
