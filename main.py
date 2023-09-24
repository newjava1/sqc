import sys
from PyQt6 import QtCore,QtWidgets,QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView,QMessageBox,QWidget
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QBrush
from ui_main import Ui_MainWindow
from ui_source_add import Ui_Dialog

import json
import os.path

import mysql.connector
import pymysql

import pandas as pd

import cx_Oracle
import platform

cx_Oracle.init_oracle_client(lib_dir="Lib/site-packages")

import psycopg2

import traceback

import sqlparse



###############################common############################# 
def getTabTitle(data):
    ip = data['ip']
    port = data['port']
    libraryName = data['instanceName']
    if len(libraryName) == 0:
        libraryName = data['libraryName']
    title = ip + ":" + port + "/" + libraryName

    return title




###############################open source############################# 

def listSource(treeView:QtWidgets.QTreeView):
    datas = getSourceList()

    treeView.setHeaderHidden(True)

    # 根节点
    treemodel = QStandardItemModel(treeView)
    rootItem = treemodel.invisibleRootItem()

    for item in datas:
        firstName = item['instanceName']
        if len(firstName)==0:
            firstName = item['libraryName']
        if len(firstName)==0:
            firstName = 'undefined'
        dbType = item['dbType']
        qStandardItem = QStandardItem(firstName)
        qStandardItem.setData(item)
        qStandardItem.setToolTip(str(item))

        dbIcon = QtGui.QPixmap('images/other.png')
        if dbType == 'mysql':
            dbIcon = QtGui.QPixmap('images/mysql.png')
            # qStandardItem.setIcon(QtGui.QIcon('images/mysql.png'))  
        elif dbType == 'oracle':
            dbIcon = QtGui.QPixmap('images/oracle.png')
            # qStandardItem.setIcon(QtGui.QIcon('images/oracle.png'))  
        elif dbType == 'postgres':
            dbIcon = QtGui.QPixmap('images/postgres.png')
            # qStandardItem.setIcon(QtGui.QIcon('images/postgres.png'))  
        scaledDbIcon = dbIcon.scaled(QtCore.QSize(100, 100))
        newDbIcon = QtGui.QIcon(scaledDbIcon)
        qStandardItem.setIcon(newDbIcon)
        font = QtGui.QFont('Times', 18)
        font.setBold(True)
        # font.setItalic(True)
        font.setUnderline(True)  
        qStandardItem.setFont(font)

        rootItem.appendRow(qStandardItem)
        
    treeView.setModel(treemodel)
    treeView.clicked.connect(lambda:open_source(treeView))



def open_source(treeView:QtWidgets.QTreeView):
    
    idx = treeView.currentIndex()
    item = treeView.model().item(idx.row(),idx.column())

    data = item.data()
    conn = getConn(data)
    if conn == None:
        QMessageBox.information(None, "info",  "conn fail, pls confirm")
        return

    # text = item.text()
    # dbType = data['dbType']
    # ip = data['ip']
    # port = data['port']
    # libraryName = data['instanceName']
    # if len(libraryName) == 0:
    #     libraryName = data['libraryName']
    title = getTabTitle(data)

    # tabs = QtWidgets.QTabWidget(ui.centralwidget, movable=True, tabsClosable=True)
    # tabs = ui.gridLayout.widgetAtPosition(0, 0)
    # QMessageBox.information(None, "info",  str(type(tabs)))

    
    tabsCount = tabs.count()
    if tabsCount > 0:
        
        i = tabsCount
        while i >= 1:
            # tabs.setCurrentIndex(i)
            tabText = tabs.tabText(i - 1)
            if tabText == title:
                tabs.setCurrentIndex(i - 1)
                return
            i = i - 1

    page1 = QWidget(tabs)
    layout = QtWidgets.QGridLayout()
    page1.setLayout(layout)
    page1.setWhatsThis(str(data))
    textBrowser = QtWidgets.QTextBrowser(page1)
    textBrowser.setReadOnly(False)
    layout.addWidget(textBrowser,0,0)

    currentIdx = tabs.addTab(page1, title)
    tabs.setCurrentIndex(currentIdx)
    # tabs.setTabText(currentIdx, title)

    # tabs.tabBar().setTabsClosable(True)
    # tabs.tabBar().setMovable(True)
    # tabs.tabCloseRequested.connect(lambda:closeTab)

    # tabsCustom.addTab(page1, title)

    # ui.gridLayout.addWidget(tabs, 0, 0, 2, 1)




name_file_sys="souceList.json"

def getSourceList():
    if not os.path.exists(name_file_sys):
        with open(name_file_sys,'w+') as f:
            pass

    datas = []
    with open(name_file_sys, 'r') as f:
        str1 = f.read()
        if str1 is not None and str1 != '':
            datas = json.loads(str1)
    return datas 

   
###############################execute sql############################# 


def execSelectedSql():
    idxTab = tabs.currentIndex()
    if idxTab == -1:
        QMessageBox.information(None, "info",  "pls choose tab")
        return
    
    currentTab = tabs.currentWidget()
    layout = currentTab.layout()
    textBrower = layout.itemAtPosition(0,0).widget()
    textCursor = textBrower.textCursor()
    sql = textCursor.selectedText()
    if len(sql) == 0:
        QMessageBox.information(None, "info",  "pls select your sql")
        return
    
    data = currentTab.whatsThis()
    
    try:
       doExecSelectedSql(eval(data), sql)
    except Exception as e:
        traceback.print_exc()


def doExecSelectedSql(data,sql):
    sql = sql.strip()
    # 解析SQL语句
    parsed = sqlparse.parse(sql)

    # 获取解析结果
    statement = parsed[0]
    
    sqlType = statement.get_type()
    if sqlType == 'SELECT':
        if data['dbType'] == 'mysql':
            executeMysql(data, sql)
        elif data['dbType'] == 'oracle':
            executeOracle(data, sql)
        elif data['dbType'] == 'postgres':
            executePostgres(data, sql)
    elif sqlType == 'INSERT' or sqlType == 'DELETE' or sqlType == 'UPDATE':
        executeNotSelect(data,sql)
    else:
        QMessageBox.information(None, "info",  "no support")
    

def executeNotSelect(data,sql):
    conn = getConn(data)
    cursor = conn.cursor()
    query = (sql)
    cursor.execute(query)
    rowcount = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    
    QMessageBox.information(None, "info",  str(rowcount))


def getConn(data):
    dbType = data['dbType']
    user = data['username']
    password = data['password']
    host = data['ip'] + ':' + data['port']
    dbName = data['instanceName']
    if len(dbName) == 0:
        dbName = data['libraryName']
    
    conn = None
    try:
        if dbType == 'mysql':
            conn = pymysql.connect(  host=data['ip'],  user=data['username'],  password=data['password'],  database=data['libraryName'])
        elif dbType == 'oracle':
            conn_str = f"{user}/{password}@{host}/{dbName}"
            conn = cx_Oracle.connect(conn_str)
        elif dbType == 'postgres':
            conn = psycopg2.connect(
            host=data['ip'],
            port=data['port'],
            dbname=dbName,
            user=user,
            password=password
        )
    except Exception as e:
        conn = None
        print('conn fail', str(e))

    return conn


def executeMysql(data,sql):
    # mysqlconnection = mysql.connector.connect(  host=data['ip'],  user=data['username'],  password=data['password'],  database=data['libraryName'])
    mysqlconnection = getConn(data)
    cursor = mysqlconnection.cursor()
    query = (sql)
    cursor.execute(query)

    renderData(cursor)
    cursor.close()
    mysqlconnection.close()


def executeOracle(data,sql):
    connect = getConn(data)
    cursor = connect.cursor()
    cursor.execute(sql)

    renderData(cursor)
    cursor.close()
    connect.close()


def executePostgres(data,sql):
    conn = getConn(data)

    cursor = conn.cursor()
    cursor.execute(sql)

    renderData(cursor)
    cursor.close()
    conn.close()

    


def renderData(cursor):
    result = cursor.fetchall()  
    col_result = cursor.description  

    columns = []
    for i in range(len(col_result)):
        columns.append(col_result[i][0])  

    df = pd.DataFrame(columns=columns)
    for i in range(len(result)):
        df.loc[i] = list(result[i])  

    print(df)
    model = PdTable(df)

    tableView = QtWidgets.QTableView()
    tableView.setStyleSheet("QTableView {border: 1px solid grey;}")
    tableView.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;color:black;}")
    tableView.setModel(model)

    currentTab = tabs.currentWidget()
    layout = currentTab.layout()
    layout.addWidget(tableView, 1, 0)

###############################add source#############################    

class PdTable (QtCore.QAbstractTableModel):
    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount (self, parent=None) :
        return self._data.shape[0]
    
    def columnCount(self, parent=None) :
        return self._data.shape[1]
    
    # show data
    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None
    
    # show head
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]
        elif orientation == QtCore.Qt.Orientation.Vertical and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data.axes[0][col]
        return None

    

def closeTab(tabs,index):
    # tabs.tabCloseRequested.emit(index)
    tabs.removeTab(index)

def closeTab2(index):
    # tabs.tabCloseRequested.emit(index)
    tabs.removeTab(index)


def setCurrentTreeItem(tabIndex):
    # tabTitle = tabs.tabText(index - 1)
    treeView = ui.treeView
    treemodel = treeView.model()
    rootItem = treemodel.invisibleRootItem()
    rowCount = rootItem.rowCount()
    i = rowCount
    while i > 0:
        childItem = rootItem.child(i - 1)
        data = childItem.data()
        title = getTabTitle(data)
        
        tabText = tabs.tabText(tabIndex)
        if tabText == title:
            modelIndex = treemodel.index(i - 1, 0)
            treeView.setCurrentIndex(modelIndex)
            return

        i = i - 1


def appendSouceList(dataTmp):
    datas = getSourceList()
    

    datas.append(dataTmp)
    # write
    with open(name_file_sys,'w+') as f:
        f.write(json.dumps(datas,indent=2,ensure_ascii=False))

    listSource(ui.treeView)
    


def saveSourceInfo(ui_addDialog:Ui_Dialog):
    ip = ui_addDialog.ipLineEdit_2.text()
    port = ui_addDialog.portLineEdit.text()
    instanceName = ui_addDialog.LineEdit.text()
    libraryName = ui_addDialog.LineEdit_2.text()
    # schemaName = ui_addDialog.LineEdit_3.text()
    username = ui_addDialog.LineEdit_4.text()
    password = ui_addDialog.LineEdit_5.text()
    dbType = ui_addDialog.LineEdit_6.text()

    dataTmp = {
        "ip": ip,
        "port": port,
        "instanceName": instanceName,
        "libraryName": libraryName,
        "username": username,
        "password": password,
        "dbType": dbType
    }
    
    # is exist
    treeView = ui.treeView
    treemodel = treeView.model()
    rootItem = treemodel.invisibleRootItem()
    rowCount = rootItem.rowCount()
    i = rowCount
    while i > 0:
        childItem = rootItem.child(i - 1)
        data = childItem.data()
        title = getTabTitle(data)
        
        if getTabTitle(dataTmp) == title:
            QMessageBox.information(None, "info",  "this info is in treeview")

            modelIndex = treemodel.index(i - 1, 0)
            treeView.setCurrentIndex(modelIndex)
            return

        i = i - 1

    # check connnection
    conn = getConn(dataTmp)
    if conn == None:
        QMessageBox.information(None, "info",  "conn fail, pls confirm")
        return
    

    appendSouceList(dataTmp)
     

def initAddSourceDialog(ui_addDialog:Ui_Dialog):
     # ui_addDialog.buttonBox.accepted.connect(lambda:saveSourceInfo(ui_addDialog))

     buttonSave = ui_addDialog.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
     buttonSave.clicked.connect(lambda:saveSourceInfo(ui_addDialog))


def openAddSourceDialog(addItem:QtGui.QAction):
     addDialog = QtWidgets.QDialog()
     ui_addDialog = Ui_Dialog()
     ui_addDialog.setupUi(addDialog)
     initAddSourceDialog(ui_addDialog)
     addDialog.exec()
        


def open_dialog(qAction:QtGui.QAction, ui_main:Ui_MainWindow):
    # sender = ui_main.sender()
    event = qAction.text()
    # QMessageBox.information(None, "info",  event)
    openAddSourceDialog(qAction)



def initMain(ui_main:Ui_MainWindow):
     # init sourcelist
    listSource(ui_main.treeView)

    # bind
    ui_main.actionmysql.triggered.connect(lambda:open_dialog(ui_main.actionmysql,ui_main))
    ui_main.actionoracle.triggered.connect(lambda:open_dialog(ui_main.actionoracle,ui_main))
    ui_main.actionpostgres.triggered.connect(lambda:open_dialog(ui_main.actionpostgres,ui_main))

    ui_main.gridLayout.addWidget(tabs, 0, 0, 2, 1)
    tabs.setTabsClosable(True)
    tabs.setMovable(True)
    # m1-use
    # tabs.tabCloseRequested.connect(lambda:closeTab(tabs,tabs.currentIndex()))
    # m2-nouse
    # tabs.tabCloseRequested.connect(closeTab)
    # m3-use
    tabs.tabCloseRequested.connect(closeTab2)
    tabs.tabBarClicked.connect(setCurrentTreeItem)
    # m4-nouse
    # tabs.tabCloseRequested.connect(lambda:closeTab2)

    # ui_main.gridLayout.addWidget(QtWidgets.QPushButton('execute'), 2, 0,
    #                           alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
    
    # spacer = QWidget()
    # spacer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
    # layout = QtWidgets.QGridLayout()
    # spacer.setLayout(layout)
    
    # execute sql
    execIcon = QtGui.QIcon("images/execute.png")
    actionExecSelectedSql = QtGui.QAction(execIcon, "doExecSelected", ui.toolBar)
    actionExecSelectedSql.triggered.connect(execSelectedSql)
    # spacer.addAction(actionExecSelectedSql)
    ui.toolBar.addAction(actionExecSelectedSql)

    # label = QtWidgets.QLabel("executee")

    # pixmap = QtGui.QPixmap("images/execute.png")
    # m_pic = execIcon.pixmap(execIcon.actualSize(QtCore.QSize(10,15)))
    # label.setPixmap(pixmap)
    # layout.addWidget(label,0,0, QtCore.Qt.AlignmentFlag.AlignCenter)
    # ui.toolBar.addWidget(spacer)

    # ui.toolBar.setStretchableWidgets(True)
    # ui.toolBar.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

    # toolbarWidth = ui.toolBar.sizeHint().width()
    # buttonWidth = ui.toolBar.widgetForAction(actionExecSelectedSql).sizeHint().width()
    # spacing = (toolbarWidth - buttonWidth * 1) / 2
    # spacing = 120
    # QMessageBox.information(None, "info",  str(spacing))
    # ui.toolBar.setContentsMargins(spacing, 0, spacing, 0)

    

app = QtWidgets.QApplication(sys.argv)
ui = Ui_MainWindow()
MainWindow = QtWidgets.QMainWindow()
ui.setupUi(MainWindow)

tabs = QtWidgets.QTabWidget(parent=ui.centralwidget, movable=True, tabsClosable=True)

def main():

    initMain(ui)

    MainWindow.showMaximized()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()