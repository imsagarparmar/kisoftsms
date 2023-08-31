from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import mysql.connector as con

smsui, _=loadUiType('sms.ui')

class MasterApp(QMainWindow,smsui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget.tabBar().setVisible(False)
        self.menubar.setVisible(False)
        self.btn1.clicked.connect(self.login)

        self.menu11.triggered.connect(self.show_add_new_student)
        self.btn_save_student.clicked.connect(self.save_student)

# Login Form
    def login(self):
        user_name=self.tb1.text()
        pwd=self.tb2.text()
        if(user_name=="admin" and pwd=="admin"):
            self.tabWidget.setCurrentIndex(0)
            self.menubar.setVisible(True)
        else:
            self.lbl_1.setText("Invalid Admin Login Details")
            QMessageBox.information(self,"School Management System","Invalid Admin Login Details, Try Again!")

# add new student
    def show_add_new_student(self):
        self.tabWidget.setCurrentIndex(2)
        self.gen_reg_number()
    def gen_reg_number(self):
        try:
            reg_no=0
            mydb=con.connect(host="localhost",user="root",password="",db="kschool")
            cur=mydb.cursor()
            cur.execute("select * from student")
            result=cur.fetchall()
            if result:
                for stud in result:
                    reg_no+=1
            self.tb11.setText(str(reg_no+1))
        except con.Error as e:
            print("Database Select Error") 
    
    # save student
    def save_student(self):
        mydb=con.connect(host="localhost",user="root",password="",db="kschool")
        cur=mydb.cursor()
        registration_num=self.tb11.text()
        full_name=self.tb12.text()
        gender=self.cb11.currentText()
        dob=self.tb13.text()
        age=self.tb14.text()
        address=self.tb15.text()
        phone=self.tb16.text()
        email=self.tb17.text()
        standard=self.cb12.currentText()
        qry=("insert into student(registration_num,full_name,gender,dob,age,address,phone,email,standard) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        value=(registration_num,full_name,gender,dob,age,address,phone,email,standard)
        cur.execute(qry,value)
        mydb.commit()

        self.label_3.setText("Student Record Saved Successfully")
        QMessageBox.information(self,"School Management System","Student Record Saved Successfully")

def master():
    myapp=QApplication(sys.argv)
    window=MasterApp()
    window.show()
    myapp.exec_()
if __name__ == '__main__':
    master()