#! /usr/bin/env python3

# Example PySide6 program -- pir -- 22.3.2021; 6.4.2021

# ******************************************************************************
# Insert licence here!


# ******************************************************************************
import sys
import re
from sys import exit

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QInputDialog, QGridLayout, \
    QLabel, QLineEdit
from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtWidgets import QToolBar, QStatusBar
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QBrush, QColor, QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt, QSortFilterProxyModel

import random, string, sys

# from TaskDetail import Ui_TaskDetailDialog

from TaskDetail_ui import TaskDetailDialog

# ******************************************************************************

app = QApplication(sys.argv)

with open(r"styles.qss") as f:
    style = f.read()
    app.setStyleSheet(style)

class MainWindow(QMainWindow):
    """ Main window of application"""

    def __init__(self):
        super().__init__()  # Invoke __init__ of QMainWindow base class

        self.setWindowTitle("EEE231 Project")

        self.setGeometry(100, 100, 600, 400)
        self.showMaximized()

        self.mainLayout = QVBoxLayout()

        # Setup menu bar & File menu
        self.fileMenu = self.menuBar().addMenu("&File")
        self.openMenuAction = self.fileMenu.addAction("&Open")
        self.openMenuAction.triggered.connect(
            self.on_open_action)    # New-style connect!
        self.fileMenu.addSeparator()
        self.quitMenuAction = self.fileMenu.addAction("&Quit")
        self.quitMenuAction.triggered.connect(self.on_quit_action)

        # Setup Column menu
        self.columnMenu = self.menuBar().addMenu("&Column")
        self.addColumnMenuAction = self.columnMenu.addAction("&Add column")
        self.addColumnMenuAction.triggered.connect(self.add_column)
        self.deleteColumnMenuAction = self.columnMenu.addAction("&Delete column")
        self.deleteColumnMenuAction.triggered.connect(self.delete_column)
        self.renameColumnMenuAction = self.columnMenu.addAction("&Edit column")
        self.renameColumnMenuAction.triggered.connect(self.column_name)
        self.columnMenu.addSeparator()
        self.enableWIPMenuAction = self.columnMenu.addAction("&Enable WIP")
        self.enableWIPMenuAction.triggered.connect(self.enable_WIP)
        self.disableWIPMenuAction = self.columnMenu.addAction("&Disable WIP")
        self.disableWIPMenuAction.triggered.connect(self.disable_WIP)
        self.editWIPMenuAction = self.columnMenu.addAction("&Edit WIP")
        self.editWIPMenuAction.triggered.connect(self.edit_WIP)

        # Setup Task menu
        self.taskMenu = self.menuBar().addMenu("&Task")
        self.addTaskMenuAction = self.taskMenu.addAction("&Add Task")
        self.addTaskMenuAction.triggered.connect(self.add_task)
        self.deleteTaskMenuAction = self.taskMenu.addAction("&Delete Task")
        self.deleteTaskMenuAction.triggered.connect(self.delete_task)
        self.taskDetailMenuAction = self.taskMenu.addAction("&Edit Task")
        self.taskDetailMenuAction.triggered.connect(self.task_detail)
        self.taskMenu.addSeparator()
        self.moveTaskMenuAction = self.taskMenu.addAction("&Move Task to Next Column")
        self.moveTaskMenuAction.triggered.connect(self.move_task)

        # Setup About menu
        self.aboutMenu = self.menuBar().addMenu("&About")
        self.aboutMenuAction = self.aboutMenu.addAction("&About")
        self.aboutMenuAction.triggered.connect(self.on_about_action)

        # Create main toolbar
        self.mainToolBar = QToolBar()
        self.mainToolBar.setMovable(False)
        self.newToolButton = self.mainToolBar.addAction("New")
        self.newToolButton.triggered.connect(self.add_tab)
        self.renameToolButton = self.mainToolBar.addAction("Rename")
        self.renameToolButton.triggered.connect(self.tab_name)
        self.openToolButton = self.mainToolBar.addAction("Open")
        self.openToolButton.triggered.connect(self.on_open_action)
        self.saveToolButton = self.mainToolBar.addAction("Save")
        self.saveAsToolButton = self.mainToolBar.addAction("Save As")
        self.saveAsToolButton.triggered.connect(self.on_saveAs_action)
        self.closeToolButton = self.mainToolBar.addAction("Close")
        self.closeToolButton.triggered.connect(self.close_tab)
        self.addToolBar(self.mainToolBar)
        self.mainLayout.addWidget(self.mainToolBar)

        #create searchbar
        self.searchbar = QLineEdit()
        #have it say something before text is entered
        self.searchbar.setPlaceholderText("Search for a Task...")
        self.searchbar.setFixedWidth(475) #set width
        #when text is changed do a search
        self.searchbar.textChanged.connect(self.searchForTask)
        self.mainLayout.addWidget(self.searchbar)

        # Create tabbed widget
        self.tabbedWidget = QTabWidget()
        self.tabbedWidget.currentChanged.connect(self.on_tab_changed)

        self.tab = QTableWidget(0, 4, self.tabbedWidget)

        # Set column headers
        columnHeadings = ["Backlog", "In progress", "Blocked", "Completed"]
        self.tab.setHorizontalHeaderLabels(columnHeadings)

        #give column headings a fixed width
        for x in range(4):
            self.tab.setColumnWidth(x, 400)

        # Set Kanban board title
        self.tabbedWidget.addTab(self.tab, "Untitled Project")
        self.mainLayout.addWidget(self.tabbedWidget)   

        # Set mainLayout as the central widget
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        # Disable Edit
        self.tabbedWidget.widget(self.tabbedWidget.currentIndex()).setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Create Lists to save task information
        self.taskNameList = [['']]
        self.taskMemberList = [['']]
        self.startTimeList = [['']]
        self.dueTimeList = [['']]
        self.taskLogList = [['']]

        # Create Flag to check if WIP is enabled
        self.flagWIPEnabled = [[0,0,0,0]]


    # --------------------------------------------------------------------------

    def search_item(self,column):
        """Count the number of non empty items in a column"""
        tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
        rowCount = tableWidget.rowCount()
        itemCount = 0
        row = 0
        while (row < rowCount):
            item = tableWidget.item(row,column)
            if item:
                itemCount += 1
            row += 1
        return itemCount

    # --------------------------------------------------------------------------

    def searchForTask(self, searchMatch):

        #set current index of tab so it works with all projects
        tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
        
        #reset search before each one
        tableWidget.setCurrentItem(None)

        #search for matching items
        matching_items = tableWidget.findItems(searchMatch, Qt.MatchContains)

        #if a match is found, highlight it in the table
        #if a match isn't found, do nothing
        if matching_items:
            item = matching_items[0]
            tableWidget.setCurrentItem(item)
        elif not searchMatch:
            return

    # --------------------------------------------------------------------------

    def check_WIP(self):
        """Check WIP"""
        tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
        tabIndex = self.tabbedWidget.currentIndex()
        columnCount = tableWidget.columnCount()
        columnIndex = 0
        while (columnIndex < columnCount):
            if self.flagWIPEnabled[tabIndex][columnIndex] == 1:
                horizontalHeader = tableWidget.horizontalHeaderItem(columnIndex).text()
                list = horizontalHeader.splitlines(False)
                print(list)
                originalHeader = list[0]
                textWIP = list[1]
                numList = re.findall(r"\d+", textWIP)
                print(numList)
                print("originalHeader:" + originalHeader)
                itemCount = self.search_item(columnIndex)
                newHeaderText = originalHeader + "\n(" + str(itemCount) + "/" + str(
                    numList[1]) + ")"
                newHeader = QTableWidgetItem(newHeaderText)
                print("newHeader:" + newHeaderText)
                tableWidget.setHorizontalHeaderItem(columnIndex, newHeader)
                # Show over WIP limit warning
                if int(itemCount) > int(numList[1]):
                    tableWidget.horizontalHeaderItem(columnIndex).setForeground(QBrush(QColor(255,0,0)))
            columnIndex += 1
        return

    # --------------------------------------------------------------------------

    def add_tab(self):
        """Add new tab"""
        tabIndex = self.tabbedWidget.currentIndex()
        self.tab = QTableWidget(0, 4, self.tabbedWidget)
        columnHeadings = ["Backlog", "In progress", "Blocked", "Completed"]
        self.tabbedWidget.addTab(self.tab,"New Project")
        self.tab.setHorizontalHeaderLabels(columnHeadings)
        self.flagWIPEnabled.append([0,0,0,0])
        self.taskNameList.append([''])
        self.taskMemberList.append([''])
        self.startTimeList.append([''])
        self.dueTimeList.append([''])
        self.taskLogList.append([''])
        print(self.flagWIPEnabled)
        print(self.taskNameList)

        for x in range(4):
            self.tab.setColumnWidth(x, 400)

        return

    # --------------------------------------------------------------------------

    def tab_name(self):
        """Change project title"""
        tabIndex = self.tabbedWidget.currentIndex()
        tabName, ok = QInputDialog.getText(self, "Project Name", "Enter project name: ")
        if tabName and ok:
            self.tabbedWidget.setTabText(tabIndex,tabName)
        return

    # --------------------------------------------------------------------------

    def close_tab(self):
        """Close current project"""
        w = QWidget()
        reply = QMessageBox.question(w, 'Close Project', 'Do you want to close this project?', QMessageBox.Close | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Close:
            tabIndex = self.tabbedWidget.currentIndex()
            self.tabbedWidget.removeTab(tabIndex)
            del self.flagWIPEnabled[tabIndex]
            del self.taskNameList[tabIndex]
            del self.taskMemberList[tabIndex]
            del self.startTimeList[tabIndex]
            del self.dueTimeList[tabIndex]
            del self.taskLogList[tabIndex]
            print(self.flagWIPEnabled)
            print(self.taskNameList)
            return
        else:
            return

    # --------------------------------------------------------------------------

    def on_open_action(self):
        """Handler for 'Open' action"""
        fileName = QFileDialog.getOpenFileName(self, "Open File", ".",("*.xml"))
        f = open(fileName[0],'rb')
        Openfiletext = f.read()
        Openfiletext = Openfiletext.rstrip()
        Openfiletext = Openfiletext.decode("utf-8")
        print(Openfiletext)
        exec(Openfiletext)

        for x in range(4):
            self.tab.setColumnWidth(x, 400)

        return
    # --------------------------------------------------------------------------
    def on_saveAs_action(self):
        """Handler for 'SaveAs' action"""
        tabIndex = self.tabbedWidget.currentIndex()
        Tabname = self.tabbedWidget.tabText(tabIndex)
        self.tablenum= self.tabbedWidget.currentWidget()
        rowCount=self.tablenum.rowCount()
        columnCount = self.tablenum.columnCount()

        labels = []
        for column in range(columnCount):
            it = self.tablenum.horizontalHeaderItem(column)
            labels.append(str(column+1) if it is None else it.text())
        labels = str(labels)

        SaveData = 'self.tab = QTableWidget('+str(rowCount)+','+str(columnCount)+ ','+ 'self.tabbedWidget)'+'\n'
        SaveData = SaveData+ 'columnHeadings = '+labels+'\n'
        SaveData = SaveData+ 'self.tabbedWidget.addTab(self.tab,"'+Tabname+'")'+'\n'
        SaveData = SaveData+ 'self.tab.setHorizontalHeaderLabels(columnHeadings)'+'\n'
        SaveData = SaveData+ 'self.flagWIPEnabled.append([0,0,0,0])'+'\n'

        SaveData = SaveData+ 'NewTabnum = self.tabbedWidget.count()-1'+'\n'
        SaveData = SaveData+ 'self.tabbedWidget.setCurrentIndex(NewTabnum)'+'\n'
        SaveData = SaveData+ 'tabIndex = self.tabbedWidget.currentIndex()'+'\n'
        SaveData = SaveData+ 'self.tablenum= self.tabbedWidget.currentWidget()'+'\n'
        SaveData = SaveData+ 'rowCount=self.tablenum.rowCount()'+'\n'
        TaskIndex = 1;

        SaveData = SaveData +'self.taskNameList.append(["",'       
        for row in range(rowCount):
            taskName=self.taskNameList[tabIndex][TaskIndex]
            SaveData = SaveData +'"'+taskName+'",'
            TaskIndex =TaskIndex+ 1;
        SaveData = SaveData[0:len(SaveData)-1]
        SaveData = SaveData + '])'+ '\n'
        TaskIndex = 1;

        SaveData = SaveData +'self.taskMemberList.append(["",'       
        for row in range(rowCount):
            taskName=self.taskMemberList[tabIndex][TaskIndex]
            SaveData = SaveData +'"'+taskName+'",'
            TaskIndex =TaskIndex+ 1;
        SaveData = SaveData[0:len(SaveData)-1]
        SaveData = SaveData + '])'+ '\n'
        TaskIndex = 1;

        SaveData = SaveData +'self.startTimeList.append(["",'       
        for row in range(rowCount):
            startTime=self.startTimeList[tabIndex][TaskIndex]
            SaveData = SaveData +'"'+startTime+'",'
            TaskIndex =TaskIndex+ 1;
        SaveData = SaveData[0:len(SaveData)-1]
        SaveData = SaveData + '])'+ '\n'
        TaskIndex = 1;

        SaveData = SaveData +'self.dueTimeList.append(["",'       
        for row in range(rowCount):
            dueTime=self.dueTimeList[tabIndex][TaskIndex]
            SaveData = SaveData +'"'+dueTime+'",'
            TaskIndex =TaskIndex+ 1;
        SaveData = SaveData[0:len(SaveData)-1]
        SaveData = SaveData + '])'+ '\n'
        TaskIndex = 1;

        SaveData = SaveData +'self.taskLogList.append(["",'       
        for row in range(rowCount):
            taskLog=self.taskLogList[tabIndex][TaskIndex]
            SaveData = SaveData +'"'+taskLog+'",'
            TaskIndex =TaskIndex+ 1;
        SaveData = SaveData[0:len(SaveData)-1]
        SaveData = SaveData + '])'+ '\n'


        for row in range(rowCount):
            for column in range(columnCount):
                widgetItem = self.tablenum.item(row,column)
                if(widgetItem and widgetItem.text):
                    SaveData = SaveData+'tableItem = QTableWidgetItem()'+'\n'
                    SaveData = SaveData + 'tableItem.setText("' + widgetItem.text()+'")'+'\n'
                    SaveData = SaveData +'self.tab.setItem('+str(row)+','+str(column)+', tableItem)'+'\n'
                else:
                    SaveData = SaveData
        print(SaveData)

        options = QFileDialog.Options()
        fileName, _= QFileDialog.getSaveFileName(self, 
            "Save File", "", "XML Files(*.xml)", options = options)       
        if fileName:
                    with open(fileName, 'w') as f:
                         f.write(SaveData)
        print("saving ", fileName[0])


        return 

    # --------------------------------------------------------------------------

    def current_row_index(self):
        """Return current row index"""
        cindex = self.tabbedWidget.widget(self.tabbedWidget.currentIndex()).currentRow()
        print(cindex)
        return cindex

    # --------------------------------------------------------------------------

    def current_column_index(self):
        """Return current column index"""
        cindex = self.tabbedWidget.widget(self.tabbedWidget.currentIndex()).currentColumn()
        print(cindex)
        return cindex

    # --------------------------------------------------------------------------

    def move_task(self):
        """Move task to the next column"""
        tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
        rowIndex = self.current_row_index()
        columnIndex = self.current_column_index()
        columnCount = tableWidget.columnCount()
        text = tableWidget.currentItem().text()
        if columnIndex < columnCount-1:
            tableWidget.setItem(rowIndex,columnIndex+1,QTableWidgetItem(text))
            tableWidget.takeItem(rowIndex,columnIndex)
        self.check_WIP()
        return

    # --------------------------------------------------------------------------

    def on_quit_action(self):
        """Handler for 'Quit' action"""
        print("quitting application")
        self.close()
        return

    # --------------------------------------------------------------------------

    def on_preferences_action(self):
        """Handler for 'Preferences' action"""
        print("running preferences")

        # Create dialog instance
        preferencesDialog = PreferencesDialog()

        # Initialise dialog controls
        preferencesDialog.lineEditControl.setText(self.randomString)

        result = preferencesDialog.exec()
        if(result == QDialog.Accepted):
            print("You pressed OK")

            # Process updated preferences
            self.randomString = preferencesDialog.lineEditControl.text()
        else:
            print("You must have pressed Cancel")
            # Ignore any updated preferences

        return

    # --------------------------------------------------------------------------

    def task_detail(self):
        """Set up task detail window"""
        taskDetail = TaskDetailDialog()
        taskIndex = self.current_row_index()+1
        tabIndex = self.tabbedWidget.currentIndex()
        if self.taskNameList[tabIndex][taskIndex]:
            taskDetail.lineEditTask.setText(self.taskNameList[tabIndex][taskIndex])
        if self.taskMemberList[tabIndex][taskIndex]:
            taskDetail.lineEditMember.setText(self.taskMemberList[tabIndex][taskIndex])
        if self.startTimeList[tabIndex][taskIndex]:
            taskDetail.lineEditStart.setDateTime(self.startTimeList[tabIndex][taskIndex])
        if self.dueTimeList[tabIndex][taskIndex]:
            taskDetail.lineEditDue.setDateTime(self.dueTimeList[tabIndex][taskIndex])
        if self.taskLogList[tabIndex][taskIndex]:
            taskDetail.plainTextEditLog.setPlainText(self.taskLogList[tabIndex][taskIndex])
            print(self.taskLogList[tabIndex])
        taskDetail.exec()
        if taskDetail.flagSave == 1:
            self.taskNameList[tabIndex][taskIndex]= taskDetail.taskName
            self.taskMemberList[tabIndex][taskIndex] = taskDetail.taskMember
            self.startTimeList[tabIndex][taskIndex] = taskDetail.startTime
            self.dueTimeList[tabIndex][taskIndex] = taskDetail.dueTime
            self.taskLogList[tabIndex][taskIndex] = taskDetail.taskLog
            task = QTableWidgetItem(self.taskNameList[tabIndex][taskIndex])
            tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
            currentItem = tableWidget.currentItem()
            tableWidget.setItem(taskIndex-1, currentItem.column(), task)

        self.check_WIP()
        return

    # --------------------------------------------------------------------------

    def on_about_action(self):
        """Handler for 'About' action"""
        QMessageBox.about(self, "About this program",
                          "This program was written as a project in 2022 for EEE231 Software Engineering at the University of Sheffield")
        return

    # --------------------------------------------------------------------------

    def on_tab_changed(self):
        """Handler for currentChanged signal of tabbedWidget object"""
        print("you just changed to tab ", self.tabbedWidget.currentIndex())
        return

    # --------------------------------------------------------------------------

    def get_column(self):
        """Get column name in list"""
        columnList = []
        columnCount = self.tabbedWidget.widget(self.tabbedWidget.currentIndex()).columnCount()
        i = 0
        while i < columnCount:
            column = self.tabbedWidget.widget(self.tabbedWidget.currentIndex()).horizontalHeaderItem(i)
            if column:
                columnHeader = column.text()
            else:
                columnHeader = ""
            columnList.append(str(i+1) + ': ' + columnHeader)
            i += 1
        return columnList

    # --------------------------------------------------------------------------

    def enable_WIP(self):
        """Enable WIP"""
        tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
        tabIndex = self.tabbedWidget.currentIndex()
        columnIndex = tableWidget.currentColumn()
        if self.flagWIPEnabled[tabIndex][columnIndex] == 0:
            limitWIP, ok = QInputDialog.getInt(self,"Set WIP Limit","Enter WIP limit: ",0)
            if ok and limitWIP:
                itemCount = self.search_item(columnIndex)
                newHeaderText = tableWidget.horizontalHeaderItem(columnIndex).text() + "\n(" + str(itemCount) + "/" + str(limitWIP) + ")"
                newHeader = QTableWidgetItem(newHeaderText)
                tableWidget.setHorizontalHeaderItem(columnIndex, newHeader)
                self.flagWIPEnabled[tabIndex][columnIndex] = 1
        self.check_WIP()
        return

    # --------------------------------------------------------------------------

    def disable_WIP(self):
        """Disable WIP"""
        tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
        tabIndex = self.tabbedWidget.currentIndex()
        columnIndex = tableWidget.currentColumn()
        if self.flagWIPEnabled[tabIndex][columnIndex] == 1:
            horizontalHeader = tableWidget.horizontalHeaderItem(columnIndex).text()
            list = horizontalHeader.splitlines(False)
            print(list)
            originalHeader = list[0]
            newHeader = QTableWidgetItem(originalHeader)
            print("newHeader:" + originalHeader)
            tableWidget.setHorizontalHeaderItem(columnIndex, newHeader)
            self.flagWIPEnabled[tabIndex][columnIndex] = 0
        self.check_WIP()
        return

    # --------------------------------------------------------------------------

    def edit_WIP(self):
        """Edit WIP"""
        tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
        tabIndex = self.tabbedWidget.currentIndex()
        columnIndex = tableWidget.currentColumn()
        if self.flagWIPEnabled[tabIndex][columnIndex] == 1:
            self.disable_WIP()
            self.enable_WIP()
        self.check_WIP()
        return

    # --------------------------------------------------------------------------

    def add_column(self):
        """Add a new column before selected column"""
        tabIndex = self.tabbedWidget.currentIndex()
        items = self.get_column()
        column, ok = QInputDialog.getItem(self,"Add Column", "Select column: ",items)
        if ok and column:
            index = items.index(column)
            tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
            tableWidget.insertColumn(index)
            self.flagWIPEnabled[tabIndex].insert(index,0)
            self.tab.setColumnWidth(index, 400)

        self.check_WIP()
        # print(self.flagWIPEnabled)
        return

    # --------------------------------------------------------------------------

    def delete_column(self):
        """Delete a selected column"""
        tabIndex = self.tabbedWidget.currentIndex()
        items = self.get_column()
        column, ok = QInputDialog.getItem(self,"Delete Column", "Select column: ",items)
        if ok and column:
            index = items.index(column)
            tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
            tableWidget.removeColumn(index)
            del self.flagWIPEnabled[tabIndex][index-1]
            print(self.flagWIPEnabled[tabIndex])
        self.check_WIP()
        return

    # --------------------------------------------------------------------------

    def column_name(self):
        """Change column name"""
        items = self.get_column()
        column, ok = QInputDialog.getItem(self, "Rename Column", "Select column: ", items)
        if ok and column:
            index = items.index(column)
            tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
            header, ok = QInputDialog.getText(self,"Column Name", "Enter column name: ")
            if ok and header:
                nameItem = QTableWidgetItem(header)
                tableWidget.setHorizontalHeaderItem(index,nameItem)
        self.check_WIP()
        return

    # --------------------------------------------------------------------------




    # --------------------------------------------------------------------------

    def add_task(self):
        """Add a new task"""
        tabIndex = self.tabbedWidget.currentIndex()
        taskDetail = TaskDetailDialog()
        taskDetail.exec()
        taskIndex = self.tabbedWidget.widget(self.tabbedWidget.currentIndex()).rowCount()
        self.taskNameList[tabIndex].append(taskDetail.taskName)
        self.taskMemberList[tabIndex].append(taskDetail.taskMember)
        self.startTimeList[tabIndex].append(taskDetail.startTime)
        self.dueTimeList[tabIndex].append(taskDetail.dueTime)
        self.taskLogList[tabIndex].append(taskDetail.taskLog)
        print(taskIndex)
        tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
        tableWidget.insertRow(taskIndex)
        task = QTableWidgetItem(self.taskNameList[tabIndex][taskIndex+1])
        tableWidget.setItem(taskIndex,0,task)
        self.check_WIP()
        print(self.taskNameList)
        print(self.flagWIPEnabled)
        return

    # --------------------------------------------------------------------------

    def delete_task(self):
        """Delete selected task"""
        tabIndex = self.tabbedWidget.currentIndex()
        rowCount = self.tabbedWidget.widget(self.tabbedWidget.currentIndex()).rowCount()
        row, ok = QInputDialog.getInt(self,"Delete Task", "Select row: ",0,1,rowCount)
        if ok and row:
            tableWidget = self.tabbedWidget.widget(self.tabbedWidget.currentIndex())
            tableWidget.removeRow(row-1)
            del self.taskNameList[tabIndex][row]
            del self.taskMemberList[tabIndex][row]
            del self.startTimeList[tabIndex][row]
            del self.dueTimeList[tabIndex][row]
            del self.taskLogList[tabIndex][row]
            print(self.taskNameList[tabIndex])
            print(self.taskMemberList[tabIndex])
            print(self.startTimeList[tabIndex])
            print(self.dueTimeList[tabIndex])
            print(self.taskLogList[tabIndex])
        self.check_WIP()
        return



# ******************************************************************************


# Main program
if __name__ == "__main__":

    mainWindow = MainWindow()
    mainWindow.show()

    exit(app.exec())

# ******************************************************************************
