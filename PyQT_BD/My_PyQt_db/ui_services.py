# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'services.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_services(object):
    def setupUi(self, Dialog_services):
        Dialog_services.setObjectName("Dialog_services")
        Dialog_services.resize(747, 432)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog_services)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableSevices = QtWidgets.QTableWidget(Dialog_services)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.tableSevices.setFont(font)
        self.tableSevices.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableSevices.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableSevices.setRowCount(0)
        self.tableSevices.setColumnCount(2)
        self.tableSevices.setObjectName("tableSevices")
        item = QtWidgets.QTableWidgetItem()
        self.tableSevices.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSevices.setHorizontalHeaderItem(1, item)
        self.tableSevices.horizontalHeader().setSortIndicatorShown(True)
        self.tableSevices.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableSevices)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btServicesAdd = QtWidgets.QPushButton(Dialog_services)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btServicesAdd.setFont(font)
        self.btServicesAdd.setObjectName("btServicesAdd")
        self.verticalLayout.addWidget(self.btServicesAdd)
        self.btServicesUpdate = QtWidgets.QPushButton(Dialog_services)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btServicesUpdate.setFont(font)
        self.btServicesUpdate.setObjectName("btServicesUpdate")
        self.verticalLayout.addWidget(self.btServicesUpdate)
        self.btServicesDel = QtWidgets.QPushButton(Dialog_services)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btServicesDel.setFont(font)
        self.btServicesDel.setObjectName("btServicesDel")
        self.verticalLayout.addWidget(self.btServicesDel)
        self.btServicdesFind = QtWidgets.QPushButton(Dialog_services)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btServicdesFind.setFont(font)
        self.btServicdesFind.setObjectName("btServicdesFind")
        self.verticalLayout.addWidget(self.btServicdesFind)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog_services)
        QtCore.QMetaObject.connectSlotsByName(Dialog_services)

    def retranslateUi(self, Dialog_services):
        _translate = QtCore.QCoreApplication.translate
        Dialog_services.setWindowTitle(_translate("Dialog_services", "Сервисные службы"))
        item = self.tableSevices.horizontalHeaderItem(0)
        item.setText(_translate("Dialog_services", "№"))
        item = self.tableSevices.horizontalHeaderItem(1)
        item.setText(_translate("Dialog_services", "Название сервисной службы"))
        self.btServicesAdd.setText(_translate("Dialog_services", "Добавить строку ..."))
        self.btServicesUpdate.setText(_translate("Dialog_services", "Обновить строку ..."))
        self.btServicesDel.setText(_translate("Dialog_services", "Удалить строку ..."))
        self.btServicdesFind.setText(_translate("Dialog_services", "Поиск ..."))

