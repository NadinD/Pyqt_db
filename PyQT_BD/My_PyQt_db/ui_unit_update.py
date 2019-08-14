# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unit_update.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_unit_update(object):
    def setupUi(self, Dialog_unit_update):
        Dialog_unit_update.setObjectName("Dialog_unit_update")
        Dialog_unit_update.setWindowModality(QtCore.Qt.WindowModal)
        Dialog_unit_update.resize(499, 363)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog_unit_update)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(5, 10, 5, 2)
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog_unit_update)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.Edit_Unit_up = QtWidgets.QLineEdit(Dialog_unit_update)
        self.Edit_Unit_up.setObjectName("Edit_Unit_up")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Edit_Unit_up)
        self.label_2 = QtWidgets.QLabel(Dialog_unit_update)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.Edit_Short_Unit_up = QtWidgets.QLineEdit(Dialog_unit_update)
        self.Edit_Short_Unit_up.setObjectName("Edit_Short_Unit_up")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Edit_Short_Unit_up)
        self.label_3 = QtWidgets.QLabel(Dialog_unit_update)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.CB_unit_up = QtWidgets.QComboBox(Dialog_unit_update)
        self.CB_unit_up.setObjectName("CB_unit_up")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.CB_unit_up)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.btnUnit_up_Ok = QtWidgets.QPushButton(Dialog_unit_update)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnUnit_up_Ok.setFont(font)
        self.btnUnit_up_Ok.setObjectName("btnUnit_up_Ok")
        self.horizontalLayout_6.addWidget(self.btnUnit_up_Ok)
        self.btnUnit_up_Cancel = QtWidgets.QPushButton(Dialog_unit_update)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnUnit_up_Cancel.setFont(font)
        self.btnUnit_up_Cancel.setObjectName("btnUnit_up_Cancel")
        self.horizontalLayout_6.addWidget(self.btnUnit_up_Cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.Edit_Id = QtWidgets.QLineEdit(Dialog_unit_update)
        self.Edit_Id.setEnabled(False)
        self.Edit_Id.setObjectName("Edit_Id")
        self.verticalLayout_2.addWidget(self.Edit_Id)
        spacerItem1 = QtWidgets.QSpacerItem(20, 173, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)

        self.retranslateUi(Dialog_unit_update)
        QtCore.QMetaObject.connectSlotsByName(Dialog_unit_update)

    def retranslateUi(self, Dialog_unit_update):
        _translate = QtCore.QCoreApplication.translate
        Dialog_unit_update.setWindowTitle(_translate("Dialog_unit_update", "Обновить данные по подразделению"))
        self.label.setText(_translate("Dialog_unit_update", "Подразделение"))
        self.label_2.setText(_translate("Dialog_unit_update", "Сокращенное \n"
"название"))
        self.label_3.setText(_translate("Dialog_unit_update", "Вышестоящие \n"
"подразделение"))
        self.btnUnit_up_Ok.setText(_translate("Dialog_unit_update", "Записать"))
        self.btnUnit_up_Cancel.setText(_translate("Dialog_unit_update", "Отмена"))
