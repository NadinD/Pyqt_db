# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unit.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_unit(object):
    def setupUi(self, Dialog_unit):
        Dialog_unit.setObjectName("Dialog_unit")
        Dialog_unit.resize(1084, 654)
        Dialog_unit.setModal(False)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog_unit)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableUnit = QtWidgets.QTableWidget(Dialog_unit)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.tableUnit.setFont(font)
        self.tableUnit.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableUnit.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableUnit.setRowCount(0)
        self.tableUnit.setColumnCount(4)
        self.tableUnit.setObjectName("tableUnit")
        item = QtWidgets.QTableWidgetItem()
        self.tableUnit.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableUnit.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableUnit.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableUnit.setHorizontalHeaderItem(3, item)
        self.tableUnit.horizontalHeader().setSortIndicatorShown(True)
        self.tableUnit.horizontalHeader().setStretchLastSection(True)
        self.tableUnit.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.tableUnit)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btUnitAdd = QtWidgets.QPushButton(Dialog_unit)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btUnitAdd.setFont(font)
        self.btUnitAdd.setObjectName("btUnitAdd")
        self.verticalLayout.addWidget(self.btUnitAdd)
        self.btUnitUpdate = QtWidgets.QPushButton(Dialog_unit)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btUnitUpdate.setFont(font)
        self.btUnitUpdate.setObjectName("btUnitUpdate")
        self.verticalLayout.addWidget(self.btUnitUpdate)
        self.btUnitDel = QtWidgets.QPushButton(Dialog_unit)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btUnitDel.setFont(font)
        self.btUnitDel.setObjectName("btUnitDel")
        self.verticalLayout.addWidget(self.btUnitDel)
        self.btUnitFind = QtWidgets.QPushButton(Dialog_unit)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btUnitFind.setFont(font)
        self.btUnitFind.setObjectName("btUnitFind")
        self.verticalLayout.addWidget(self.btUnitFind)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog_unit)
        QtCore.QMetaObject.connectSlotsByName(Dialog_unit)

    def retranslateUi(self, Dialog_unit):
        _translate = QtCore.QCoreApplication.translate
        Dialog_unit.setWindowTitle(_translate("Dialog_unit", "Справочник подразделений"))
        item = self.tableUnit.horizontalHeaderItem(0)
        item.setText(_translate("Dialog_unit", "№"))
        item = self.tableUnit.horizontalHeaderItem(1)
        item.setText(_translate("Dialog_unit", "Название подразделения"))
        item = self.tableUnit.horizontalHeaderItem(2)
        item.setText(_translate("Dialog_unit", "Сокращенное название"))
        item = self.tableUnit.horizontalHeaderItem(3)
        item.setText(_translate("Dialog_unit", "Вышестоящее подразделение"))
        self.btUnitAdd.setText(_translate("Dialog_unit", "Добавить строку ..."))
        self.btUnitUpdate.setText(_translate("Dialog_unit", "Обновить строку ..."))
        self.btUnitDel.setText(_translate("Dialog_unit", "Удалить строку ..."))
        self.btUnitFind.setText(_translate("Dialog_unit", "Поиск ..."))
