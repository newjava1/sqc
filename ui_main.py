# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(795, 571)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.treeView = QtWidgets.QTreeView(parent=self.centralwidget)
        self.treeView.setObjectName("treeView")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.treeView)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 795, 22))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(parent=self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionother = QtGui.QAction(parent=MainWindow)
        self.actionother.setObjectName("actionother")
        self.actionmysql = QtGui.QAction(parent=MainWindow)
        self.actionmysql.setObjectName("actionmysql")
        self.actionoracle = QtGui.QAction(parent=MainWindow)
        self.actionoracle.setObjectName("actionoracle")
        self.actionpostgres = QtGui.QAction(parent=MainWindow)
        self.actionpostgres.setObjectName("actionpostgres")
        self.menu.addAction(self.actionmysql)
        self.menu.addAction(self.actionoracle)
        self.menu.addAction(self.actionpostgres)
        self.menu.addAction(self.actionother)
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.menu.setTitle(_translate("MainWindow", "新增数据库"))
        self.menu.setTitle(_translate("MainWindow", "add source"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionother.setText(_translate("MainWindow", "other"))
        self.actionmysql.setText(_translate("MainWindow", "mysql"))
        self.actionoracle.setText(_translate("MainWindow", "oracle"))
        self.actionpostgres.setText(_translate("MainWindow", "postgres"))