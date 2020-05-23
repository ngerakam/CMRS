from __future__ import print_function

__author__ = 'Dennis Ngera'

import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog
import sys

#====== the below import helps to view ui files ============

from PyQt5.uic import loadUiType

import sqlite3

import random
import string

import datetime

import re

ui,_ = loadUiType('crms.ui')
login,_ = loadUiType('login.ui')

conn = sqlite3.connect('db.sqlite3')

c_cur = conn.cursor()

email_format = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

phone_format = re.compile(r'^[0]+[7]+\d+$')

nid_format = re.compile(r'\d+$')

date_format = re.compile(r'^(0[1-9]|[12][0-9]|3[01])+[- /.](0[1-9]|1[012])+[- /.](19|20)\d\d+$')

name_format = re.compile(r"^[a-zA-Z']+$")



#==========================class that generates random integers===================#

class reg_num:
	def random_string(length=6):
		return ''.join(random.choice(string.digits) for x in range(length))
		#print(random_digit())
		

#===============class that is loaded first when the programe runs================#

class Login(QWidget, login):
	def __init__(self):
		QWidget.__init__(self)
		self.setupUi(self)
		self.pushButton.clicked.connect(self.Handle_Login)
		self.QDark_Theme()

	def Handle_Login(self):

		self.conn = conn
		self.cur = c_cur

		self.username = self.lineEdit.text()
		self.password = self.lineEdit_2.text()

		sql= " SELECT * FROM Taskmanager_admin1 "

		self.cur.execute(sql)
		data = self.cur.fetchall()

		for row in data:
			if self.username == row[2] and self.password == row[7]:
				#print('Successfully loged in')
				self.window2 = MainApp()
				self.close()
				self.window2.show()

			else:
				self.label.setText("Make sure Username and Password are correct")

	def QDark_Theme(self):
		style = open('themes/qdark.css', 'r')
		style = style.read()
		self.setStyleSheet(style)


#=============class loaded after an admin logs into the system===============#

class MainApp(QMainWindow, ui):
	def __init__(self):
		QMainWindow.__init__(self)
		self.setupUi(self)

		self.Handle_Ui_changes()
		self.Handle_Buttons()
		self.Show_Themes()
		self.Hide_Themes()
		
		self.Open_Controlpanel_Tab()
		self.Open_Patient_Registration_Tab()
		self.Open_Settings_Tab()
		
		self.Open_Insert_Tab()
		self.Open_View_Tab()
		
		#self.Login_setting()
		#self.Edit_User()

		self.QDark_Theme()

	def Handle_Ui_changes(self):
		self.Hide_Themes()
		self.tabWidget_2.tabBar().setVisible(True)
		self.tabWidget.tabBar().setVisible(False)

	def Handle_Buttons(self):
		self.pushButton_4.clicked.connect(self.Show_Themes)
		self.pushButton_14.clicked.connect(self.Hide_Themes)

		self.pushButton.clicked.connect(self.Open_Controlpanel_Tab)
		self.pushButton_2.clicked.connect(self.Open_Patient_Registration_Tab)
		self.pushButton_3.clicked.connect(self.Open_Settings_Tab)

		self.pushButton_5.clicked.connect(self.Open_Insert_Tab)
		self.pushButton_6.clicked.connect(self.Open_View_Tab)
		
		self.pushButton_10.clicked.connect(self.Add_Record)
		self.pushButton_9.clicked.connect(self.View_Record)
	  
		self.pushButton_29.clicked.connect(self.Add_Patient)
		
		self.pushButton_30.clicked.connect(self.Login_setting)
		self.pushButton_31.clicked.connect(self.Edit_User)

		self.pushButton_47.clicked.connect(self.Classic_Theme)
		self.pushButton_46.clicked.connect(self.Dark_Blue_Theme)
		self.pushButton_48.clicked.connect(self.Dark_Grey_Theme)
		self.pushButton_49.clicked.connect(self.Dark_Orange_Theme)
		self.pushButton_51.clicked.connect(self.QDark_Theme)
		self.pushButton_50.clicked.connect(self.Dark_Theme)

		self.pushButton_13.clicked.connect(self.x_ray)

	def Show_Themes(self):
		self.groupBox_4.show()

	def Hide_Themes(self):
		self.groupBox_4.hide()

############### new feature - adding an X-ray image #######################
	def x_ray(self):
		self.filename = QFileDialog.getOpenFileNames(self, ' Open file ', os.getenv('HOME'))
		
		self.Mselect = self.filename[0]

		try:
			self.select = self.Mselect[0]

		except IndexError:
			pass
		self.lineEdit_18.setText(str(self.select))	

		return self.select

	def my_xray(self):
		this = self.select
		filename_1 = open(this, 'rb')
		look = filename_1.read()

		return look   

		#########=============== Opening Tabs================###########################

	def Open_Controlpanel_Tab(self):
		self.tabWidget.setCurrentIndex(0)

	def Open_Patient_Registration_Tab(self):
		self.tabWidget.setCurrentIndex(1)

	def Open_Settings_Tab(self):
		self.tabWidget.setCurrentIndex(2)

		#######=========== Opening Tabs on the Controlpanel Tab =============##############

	def Open_Insert_Tab(self):
		self.tabWidget_2.setCurrentIndex(0)

	def Open_View_Tab(self):
		self.tabWidget_2.setCurrentIndex(1)

	

	########################################################################################################
	##########============== Control Panel ===========================######################################

	def Add_Record(self):

		self.conn = conn
		self.cur = c_cur

		#######=========== variables ===========##########3333
		
		self.prescription = self.lineEdit_11.text()
		self.national_id = self.lineEdit_4.text()
		self.hospital = self.lineEdit_5.text()
		self.county = self.comboBox.currentText()
		self.sub_county = self.lineEdit_7.text()
		self.doctor_name = self.lineEdit_8.text()
		self.doctor_id = self.lineEdit_9.text()
		self.treatment = self.lineEdit_10.text()



		if self.prescription == '' or self.national_id == '' or self.hospital == '' or self.county == '' or self.sub_county == '' or self.doctor_name == '' or self.doctor_id == '' or self.treatment == '':
			self.the_message = QMessageBox.about(self, "WARNING!!!", "Please insert values to proceed")
			
			self.w =  self.statusBar()
			self.p = self.w.palette()
			self.p.setColor(self.w.backgroundRole(), Qt.red)
			self.w.setPalette(self.p)

			self.w.showMessage('Record was unsuccessful.')

		elif not nid_format.match(self.national_id):
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter the correct national id format i.e numbers")

		elif len(self.national_id) != 8:
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter 8 digits for the ID number")

		else:

			self.record_id = reg_num.random_string()

			self.date = datetime.datetime.now()
			self.date.strftime('%d/%m/%y %H:%M:%S')

			try:
				self.national_id = int(self.national_id)
			except ValueError:
				self.message = QMessageBox.about(self, "Please ...", "Make sure you enter the correct national id format i.e numbers")

			self.record_id = int(self.record_id)

			vrfy_sql = " SELECT * FROM Taskmanager_patient WHERE national_id LIKE ? "

			self.cur.execute(vrfy_sql,(self.national_id,))

			chck_data = self.cur.fetchone()

			if chck_data:

				self.xray = self.my_xray()

				sql1 = " INSERT INTO Taskmanager_records(record_id, hospital, county, subcounty, doctor_id, doctor_name, treatment, prescription, national_id_id, date, x_ray) VALUES (?,?,?,?,?,?,?,?,?,?,?) "

				self.cur.execute(sql1, 
					(self.record_id, self.hospital, self.county, self.sub_county, self.doctor_id, self.doctor_name, self.treatment, self.prescription, self.national_id, self.date, self.xray)
				)

				self.conn.commit()
				self.w =  self.statusBar()
				self.p = self.w.palette()
				self.p.setColor(self.w.backgroundRole(), Qt.green)
				self.w.setPalette(self.p)

				self.w.showMessage('New record added successfully')

				self.lineEdit_11.setText('')
				self.lineEdit_4.setText('')
				self.lineEdit_5.setText('')
				self.comboBox.setCurrentIndex(0)
				self.lineEdit_7.setText('')
				self.lineEdit_8.setText('')
				self.lineEdit_9.setText('')
				self.lineEdit_10.setText('')
				self.lineEdit_18.setText('3')

			else:
				self.message = QMessageBox.about(self, " WARNING ", "The patient is not registered in this system")
		   

	def View_Record(self):
		self.conn = conn
		self.c_cur = c_cur
		

		search_item = self.lineEdit.text()
		
		if search_item == '':

			self.report = QMessageBox.about(self,"WARNING!!!", "Please Enter a search item")

		elif not nid_format.match(search_item):
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter the correct national id format i.e numbers")

		elif len(search_item) != 8:
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter 8 digits for the ID number")

		else:
			try:
				search_item = int(search_item)
			except ValueError:
				self.message = QMessageBox.about(self, "Please ...", "Make sure you enter the correct search item format i.e numbers")
				self.lineEdit.setText('')

			sql = " SELECT * FROM Taskmanager_records WHERE national_id_id LIKE ? "
			
			self.data = self.c_cur.execute(sql,(search_item,))

		
			self.tableWidget.setRowCount(0)
			self.tableWidget.insertRow(0)

			for row, form in enumerate(self.data):
				for column, item in enumerate(form):
					self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

					column += 1
				row_pos = self.tableWidget.rowCount()
				self.tableWidget.insertRow(row_pos)

			
   
	########################################################################################################
	##########============== Patient Registration ===========================###############################

	def Add_Patient(self):
		
		self.conn = conn
		self.c_cur = c_cur

		self.firstname = self.lineEdit_69.text()
		self.middlename = self.lineEdit_62.text()
		self.surname = self.lineEdit_63.text()
		self.nationalid = self.lineEdit_67.text()
		
		self.phone_num = self.lineEdit_68.text()
		self.address = self.lineEdit_70.text()
		self.d_o_b = self.lineEdit_71.text()
		self.email = self.lineEdit_72.text()

		####################============== the patient id generated randomly by the reg_num class =====####
		self.p_id = reg_num.random_string()

		self.time = datetime.datetime.now()
		self.time.strftime('%d/%m/%y %H:%M:%S')

		if self.firstname == '' or self.middlename == '' or self.surname == '' or self.nationalid =='' or self.phone_num == '' or self.address == '' or self.d_o_b == '' or self.email == '':

			self.message = QMessageBox.about(self, "Please ...", "Make sure no field is empty")
			
			#print('No input ...')

			self.w =  self.statusBar()
			self.p = self.w.palette()
			self.p.setColor(self.w.backgroundRole(), Qt.red)
			self.w.setPalette(self.p)

			self.w.showMessage('Action was unsuccessful.')

			self.lineEdit_69.setText('')
			self.lineEdit_62.setText('')
			self.lineEdit_63.setText('')
			self.lineEdit_67.setText('')
			self.lineEdit_68.setText('')
			self.lineEdit_70.setText('')
			self.lineEdit_71.setText('')
			self.lineEdit_72.setText('')

		elif not nid_format.match(self.nationalid):
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter the correct national id format i.e numbers")
			
		elif len(self.nationalid) != 8:
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter 8 digits for the ID number")

		elif not phone_format.match(self.phone_num):
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter the correct phone format i.e o7***34**0 ")
			
		elif len(self.phone_num) != 10:
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter 10 digits for the phone number")

		elif not email_format.match(self.email):
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter the correct email")
		
		elif not date_format.match(self.d_o_b):
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter the correct date format i.e dd/mm/yyyy or dd-mm-yyyy")

		elif not name_format.match(self.firstname):
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter a valid first name")

		elif not name_format.match(self.middlename):
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter a valid middle name")

		elif not name_format.match(self.surname):
			self.message = QMessageBox.about(self, "Please ...", "Make sure you enter a valid surname name")

		else:
			try:
				self.nationalid = int(self.nationalid)
			except ValueError:
				pass

			chck_sql = " SELECT * FROM Taskmanager_patient WHERE national_id LIKE ? "

			self.c_cur.execute(chck_sql,(self.nationalid,))

			vrfy_data = self.c_cur.fetchone()

			if vrfy_data:
				self.message = QMessageBox.about(self, " WARNING ", "The patient with this ID number already exists in the system")

			else:

				sql = " INSERT INTO Taskmanager_patient (patient_id, first_name, middle_name, surname, national_id, phone_number, address, date_of_birth, email, date_registered) VALUES(?,?,?,?,?,?,?,?,?,?)"

				self.c_cur.execute(sql ,
						(self.p_id, self.firstname, self.middlename, self.surname, self.nationalid, self.phone_num, self.address, self.d_o_b, self.email, self.time )
				)

				self.conn.commit()
				
				self.w =  self.statusBar()
				self.p = self.w.palette()
				self.p.setColor(self.w.backgroundRole(), Qt.green)
				self.w.setPalette(self.p)

				self.w.showMessage('Patient registered successfully.')
				#print('Successfully added to the database')

				self.lineEdit_69.setText('')
				self.lineEdit_62.setText('')
				self.lineEdit_63.setText('')
				self.lineEdit_67.setText('')
				self.lineEdit_68.setText('')
				self.lineEdit_70.setText('')
				self.lineEdit_71.setText('')
				self.lineEdit_72.setText('')

	########################################################################################################
	##########============== Settings ===========================###########################################

	def Login_setting(self):
		self.conn = conn
		self.c_cur = c_cur

		self.username = self.lineEdit_73.text()
		self.mypassword = self.lineEdit_74.text()

		if self.username == '' or self.mypassword == '':
				self.message = QMessageBox.about(self, "Please ...", "Make there is no empty field")

		else:
			sql = " SELECT * FROM Taskmanager_admin1 WHERE username = ? and password = ?"

			self.c_cur.execute(sql ,
							(self.username,self.mypassword) 
							)

			data = self.c_cur.fetchone()

			if data:

				self.lineEdit_76.setText(data[2])
				self.lineEdit_78.setText(data[6])
				self.lineEdit_77.setText(data[5])
				self.lineEdit_75.setText(data[7])

				self.lineEdit_73.setText('')
				self.lineEdit_74.setText('')

			else:
				self.message = QMessageBox.about(self, "WARNING!!!", "This user does not exist")
				self.lineEdit_73.setText('')
				self.lineEdit_74.setText('')

	def Edit_User(self):
		self.conn = conn
		self.c_cur = c_cur

		self.myUser = self.lineEdit_76.text()
		self.myemail = self.lineEdit_78.text()
		self.myphone = self.lineEdit_77.text()
		self.thepass = self.lineEdit_75.text()

		if self.myUser == '' or self.myemail == '' or self.myphone == '' or self.thepass == '':
			self.message = QMessageBox.about(self, "Please ...", "Make there is no empty field")

		else:

			sql = " UPDATE Taskmanager_admin1 SET username = ?, email = ?, phone_number = ?, password = ? "

			self.c_cur.execute(sql , (self.myUser, self.myemail, self.myphone, self.thepass))

			self.conn.commit()

			self.w =  self.statusBar()
			self.p = self.w.palette()
			self.p.setColor(self.w.backgroundRole(), Qt.green)
			self.w.setPalette(self.p)
			self.w.showMessage('Your settings updated successfully.')

			self.lineEdit_76.setText('')
			self.lineEdit_78.setText('')
			self.lineEdit_77.setText('')
			self.lineEdit_75.setText('')
	

########################################################################################################
	##########============== UI THEMES ===========================###############################
	def Dark_Grey_Theme(self):
		style = open('themes/darkgrey.css', 'r')
		style = style.read()
		self.setStyleSheet(style)

	def Dark_Orange_Theme(self):
		style = open('themes/darkorange.css', 'r')
		style = style.read()
		self.setStyleSheet(style)

	def Dark_Blue_Theme(self):
		style = open('themes/darkblue.css', 'r')
		style = style.read()
		self.setStyleSheet(style)

	def Classic_Theme(self):
		style = open('themes/classic.css', 'r')
		style = style.read()
		self.setStyleSheet(style)

	def QDark_Theme(self):
		style = open('themes/qdark.css', 'r')
		style = style.read()
		self.setStyleSheet(style)

	def Dark_Theme(self):
		style = open('themes/dark.css', 'r')
		style = style.read()
		self.setStyleSheet(style)

	#def Light_Theme(self):
	   # style = open('themes/light.css', 'r')
		#style = style.read()
		#self.setStyleSheet(style)


def main():
	app = QApplication(sys.argv)
	window = Login()
	window.show()
	sys.exit(app.exec_())

if __name__ =='__main__':
	main()
