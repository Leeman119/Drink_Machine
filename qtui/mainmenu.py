# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainmenu.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainMenu(object):
    def setupUi(self, MainMenu):
        MainMenu.setObjectName("MainMenu")
        MainMenu.resize(760, 345)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../images/icons/Bronx.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainMenu.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_drink = QtWidgets.QPushButton(self.centralwidget)
        self.btn_drink.setMinimumSize(QtCore.QSize(250, 50))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.btn_drink.setFont(font)
        self.btn_drink.setObjectName("btn_drink")
        self.verticalLayout.addWidget(self.btn_drink)
        self.btn_recipe = QtWidgets.QPushButton(self.centralwidget)
        self.btn_recipe.setMinimumSize(QtCore.QSize(250, 50))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.btn_recipe.setFont(font)
        self.btn_recipe.setObjectName("btn_recipe")
        self.verticalLayout.addWidget(self.btn_recipe)
        self.btn_bar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_bar.setMinimumSize(QtCore.QSize(250, 50))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.btn_bar.setFont(font)
        self.btn_bar.setObjectName("btn_bar")
        self.verticalLayout.addWidget(self.btn_bar)
        self.btn_pump = QtWidgets.QPushButton(self.centralwidget)
        self.btn_pump.setMinimumSize(QtCore.QSize(250, 50))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.btn_pump.setFont(font)
        self.btn_pump.setObjectName("btn_pump")
        self.verticalLayout.addWidget(self.btn_pump)
        self.btn_exit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exit.setMinimumSize(QtCore.QSize(250, 50))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.btn_exit.setFont(font)
        self.btn_exit.setObjectName("btn_exit")
        self.verticalLayout.addWidget(self.btn_exit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        MainMenu.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainMenu)
        self.statusbar.setObjectName("statusbar")
        MainMenu.setStatusBar(self.statusbar)

        self.retranslateUi(MainMenu)
        QtCore.QMetaObject.connectSlotsByName(MainMenu)

    def retranslateUi(self, MainMenu):
        _translate = QtCore.QCoreApplication.translate
        MainMenu.setWindowTitle(_translate("MainMenu", "Drink Machine"))
        self.btn_drink.setText(_translate("MainMenu", "Drink!"))
        self.btn_recipe.setText(_translate("MainMenu", "Recipe Book"))
        self.btn_bar.setText(_translate("MainMenu", "Bar Stock"))
        self.btn_pump.setText(_translate("MainMenu", "Pump Setup"))
        self.btn_exit.setText(_translate("MainMenu", "Exit"))

