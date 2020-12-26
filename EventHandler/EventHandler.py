import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from EventHandlerUi import Ui_MainWindow
import pandas as pd
import numpy as np
import os

class window(QMainWindow):
	
	if os.path.exists(os.getcwd()+"\\AllEvents.csv") == False:
		allevents = pd.DataFrame(dict(date=[],time=[],event=[]))
		file = open(os.getcwd()+"\\AllEvents.csv",'x')
		file.close()
		allevents.to_csv(os.getcwd()+"\\AllEvents.csv",index=False)
	allevents = pd.read_csv(os.getcwd()+"\\AllEvents.csv")
	
	def __init__(self,parent=None):
		super(window,self).__init__(parent = None)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.dispEvent()
		
		#Calendar related
		self.ui.calendarWidget.clicked[QDate].connect(self.dispEvent)
		
		#Event(s) Tab
		self.ui.pushButton_2.clicked.connect(self.refreshEvents)
		
		#Add event(s) Tab
		self.ui.comboBox.addItems(["AM","PM"])
		self.ui.pushButton.clicked.connect(self.addEvent)
		
		self.ui.tabWidget.currentChanged.connect(self.clear)
		
		self.ui.listWidget.itemClicked.connect(self.deleteItem)
	
	def clear(self):
		self.ui.label_5.setText('')
		self.ui.lineEdit.setText('')
		self.ui.spinBox.setValue(1)
		self.ui.spinBox_2.setValue(0)
	
	def dispEvent(self):
		eventlist = ""
		listofevents = []
		window.allevents.replace(np.nan,'')
		date = QDate(self.ui.calendarWidget.selectedDate())
		Date = date.toString()
		ct=0
		for d in window.allevents['date'].tolist():
			if d==Date:
				time_ = window.allevents['time'].tolist()[ct]
				ev = window.allevents['event'].tolist()[ct]
				listofevents.append(time_+" - "+ev)
			ct+=1
		listofevents.sort()
		self.ui.listWidget.clear()
		for x in listofevents:
			self.ui.listWidget.addItem(x)

	def addEvent(self):
		date = QDate(self.ui.calendarWidget.selectedDate())
		Date = date.toString()
		eventdescrp = self.ui.lineEdit.text()
		eventdescrp = eventdescrp.strip()
		if eventdescrp.strip()=='':
			self.ui.label_5.setText("Description required.")
			return
		hour = self.ui.spinBox.text()
		minutes = self.ui.spinBox_2.text()
		timeofday = self.ui.comboBox.currentText()
		if len(minutes)==1:
			minutes = "0"+minutes
		time = hour+":"+minutes
		time = time.strip()
		window.allevents.loc[len(window.allevents.index)] = [Date,f"{time} {timeofday}",eventdescrp]
		window.allevents.to_csv(os.getcwd()+"\\AllEvents.csv",index=False)
		window.allevents = pd.read_csv(os.getcwd()+"\\AllEvents.csv")
		self.ui.label_5.setText("New event added.")
		
	def deleteItem(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Question)
		msg.setText("Do you want to delete this entry?")
		msg.setWindowTitle("Delete event")
		msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		msg.buttonClicked.connect(self.confirmation)
		
		btn = msg.exec_()
		
		date = QDate(self.ui.calendarWidget.selectedDate())
		Date = date.toString()
		listevents = self.ui.listWidget.currentItem().text().split("-")
		eventt = listevents[1].strip()
		timee = listevents[0].strip()
		if btn == QMessageBox.Ok:
			df = window.allevents
			df_new = df.drop(df[(df['date'] == Date) & (df['event'] == eventt) & (df['time'] == timee)].index)
			window.allevents = df_new
			window.allevents.to_csv(os.getcwd()+"\\AllEvents.csv",index=False)
			window.allevents = pd.read_csv(os.getcwd()+"\\AllEvents.csv")
			self.dispEvent()
		else:
			return
		
	def confirmation(self,btn):
		pass
		
	
	def refreshEvents(self):
		self.dispEvent()

def main():
	app = QApplication(sys.argv)
	ex = window()
	ex.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
