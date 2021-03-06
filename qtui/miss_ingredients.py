# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'miss_ingredients.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MissingIngredients(object):
    def setupUi(self, MissingIngredients):
        MissingIngredients.setObjectName("MissingIngredients")
        MissingIngredients.resize(800, 480)
        font = QtGui.QFont()
        font.setPointSize(8)
        MissingIngredients.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../images/icons/Bronx.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MissingIngredients.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(MissingIngredients)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(MissingIngredients)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(MissingIngredients)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 365, 315))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.dsp_miss_ingredients = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.dsp_miss_ingredients.setText("")
        self.dsp_miss_ingredients.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.dsp_miss_ingredients.setWordWrap(True)
        self.dsp_miss_ingredients.setObjectName("dsp_miss_ingredients")
        self.verticalLayout_4.addWidget(self.dsp_miss_ingredients)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(MissingIngredients)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.groupBox_2)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 365, 315))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.dsp_instructions = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.dsp_instructions.setText("")
        self.dsp_instructions.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.dsp_instructions.setWordWrap(True)
        self.dsp_instructions.setObjectName("dsp_instructions")
        self.verticalLayout_5.addWidget(self.dsp_instructions)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.addWidget(self.scrollArea_2)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_stop = QtWidgets.QPushButton(MissingIngredients)
        self.btn_stop.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btn_stop.setFont(font)
        self.btn_stop.setObjectName("btn_stop")
        self.horizontalLayout.addWidget(self.btn_stop)
        self.btn_ok = QtWidgets.QPushButton(MissingIngredients)
        self.btn_ok.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btn_ok.setFont(font)
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout.addWidget(self.btn_ok)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MissingIngredients)
        QtCore.QMetaObject.connectSlotsByName(MissingIngredients)

    def retranslateUi(self, MissingIngredients):
        _translate = QtCore.QCoreApplication.translate
        MissingIngredients.setWindowTitle(_translate("MissingIngredients", "Add Missing Ingredients"))
        self.label.setText(_translate("MissingIngredients", "Message"))
        self.groupBox.setTitle(_translate("MissingIngredients", "Missing Ingredients"))
        self.groupBox_2.setTitle(_translate("MissingIngredients", "Instructions"))
        self.btn_stop.setText(_translate("MissingIngredients", "STOP!!"))
        self.btn_ok.setText(_translate("MissingIngredients", "Ok"))

