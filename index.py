from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from MainWindow import Ui_MainWindow as MainWin
from LoginWindow import Ui_MainWindow as LoginWin
from externel_lib.exel_Client import Export
from sys import argv
import sqlite3
import datetime


a_user_name = 0
class ui(QMainWindow,MainWin):
    def __init__(self,parent = None):
        super(ui, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ui_chenge()
        self.handling_button()
        self.db = sqlite3.connect('Data_base/data.db')
        self.cur = self.db.cursor()
        self.show_all_client()
        self.show_all_historiq()
        self.com()


    def ui_chenge (self):

        self.setWindowTitle("djana horiya")
        self.tabWidget.tabBar().setVisible(False)
        self.setFixedSize(QSize(994,550))
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def handling_button (self):
        self.pushButton.clicked.connect(self.today_work_tab)
        self.pushButton_2.clicked.connect(self.historiq_tab)
        self.pushButton_3.clicked.connect(self.setting_tab)
        self.pushButton_4.clicked.connect(self.EXport_clients)

        self.pushButton_13.clicked.connect(self.add_user)
        self.pushButton_15.clicked.connect(self.seartch_edit_user)
        self.pushButton_16.clicked.connect(self.edit_user)
        self.pushButton_17.clicked.connect(self.delete_user)


        self.pushButton_9.clicked.connect(self.add_client)
        self.pushButton_12.clicked.connect(self.seart_edit_client)
        self.pushButton_10.clicked.connect(self.edit_client)
        self.pushButton_11.clicked.connect(self.delete_client)
        self.pushButton_5.clicked.connect(self.sertshe_client)

        self.pushButton_6.clicked.connect(self.seartch_historiq)
        self.pushButton_7.clicked.connect(self.Export_hestory)

        self.pushButton_8.clicked.connect(self.logout)

    def today_work_tab (self):
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_3.setCurrentIndex(0)
        self.show_all_client()

    def historiq_tab (self):
        self.tabWidget.setCurrentIndex(2)
        self.show_all_historiq()

    def setting_tab (self):
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_2.setCurrentIndex(0)
        ###################################################################################################################################
        ###############################clients

    def add_client(self):
        client_parent_name = self.lineEdit_2.text()
        client_Child_name = self.lineEdit_3.text()
        client_phone = self.lineEdit_4.text()
        client_national_id = self.lineEdit_5.text()
        pay_prise_of_subscription = self.comboBox_4.currentIndex()
        time = datetime.datetime.now()
        action = 0
        global a_user_name

        self.cur.execute('''INSERT INTO Clients (client_parent_name ,client_Child_name , client_phone,client_national_id, client_Subscription_time ,pay_prise_of_subscription )
                    VALUES (?,?,?,?,?,?)''' , (client_parent_name,client_Child_name,client_phone,client_national_id,time,pay_prise_of_subscription))
        self.cur.execute('''INSERT INTO historiq (user_id , action , time )
                        VALUES (?,?,?)''',(a_user_name,action,time))
        self.db.commit()
        self.show_all_client()
        self.show_all_historiq()

    def seart_edit_client(self):
        try:
            client_national_id = self.lineEdit_10.text()
            self.cur.execute('''SELECT client_parent_name ,client_Child_name , client_phone,client_national_id,pay_prise_of_subscription  FROM Clients WHERE client_national_id = ?''',(client_national_id,))
            data = self.cur.fetchone()
            self.lineEdit_8.setText(data[0])
            self.lineEdit_9.setText(data[1])
            self.lineEdit_7.setText(str(data[2]))
            self.lineEdit_6.setText(str(data[3]))
            self.comboBox_5.setCurrentIndex(data[4])
            self.groupBox_3.setEnabled(True)
        except Exception :
            self.null_error()
        else:
            self.lineEdit_10.setText("")

    def null_error(self) :
        pass

    def edit_client(self):
        client_parent_name = self.lineEdit_8.text()
        client_Child_name = self.lineEdit_9.text()
        client_phone = self.lineEdit_7.text()
        client_national_id = self.lineEdit_6.text()
        pay_prise_of_subscription = self.comboBox_5.currentIndex()
        client_Subscription_time = datetime.datetime.now()
        self.cur.execute('''UPDATE Clients SET client_parent_name = ? , client_Child_name = ? , client_phone = ?, client_national_id = ? , client_Subscription_time = ? , pay_prise_of_subscription = ? WHERE client_national_id = ?
        ''',(client_parent_name,client_Child_name,client_phone,client_national_id,client_Subscription_time,pay_prise_of_subscription,client_national_id))
        self.db.commit()
        self.show_all_client()
        print("done")

    def delete_client(self):

        client_national_id = self.lineEdit_6.text()
        client_Child_name = self.lineEdit_9.text()
        self.cur.execute('''DELETE FROM Clients WHERE client_national_id = ? AND client_Child_name = ? ''',(client_national_id,client_Child_name))
        self.db.commit()
        print("done delete")
        self.show_all_client()

    def show_all_client(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        self.cur.execute('''SELECT client_parent_name ,client_Child_name , client_phone,client_national_id,pay_prise_of_subscription  FROM Clients''')
        data = self.cur.fetchall()

        for row,form in enumerate(data):

            for column , forme in enumerate(form):
                if column == 4 :
                    if forme == 0 :
                        aa = "Yes"
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str(aa)))
                    else:
                        aa = "No"
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str(aa)))
                else :
                    self.tableWidget.setItem(row,column,QTableWidgetItem(str(forme)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    def sertshe_client(self):
        try :
            client_national_id = self.lineEdit.text()
            set_ani = self.comboBox.currentIndex()
            if set_ani == 0 :
                self.cur.execute('''SELECT client_parent_name ,client_Child_name , client_phone,client_national_id,pay_prise_of_subscription FROM Clients WHERE client_national_id = ?''',(client_national_id,))
                data = self.cur.fetchall()
            elif set_ani == 1:
                self.cur.execute('''SELECT client_parent_name ,client_Child_name , client_phone,client_national_id,pay_prise_of_subscription FROM Clients WHERE pay_prise_of_subscription = ?''',(0,))
                data = self.cur.fetchall()
            elif set_ani == 2:
                self.cur.execute('''SELECT client_parent_name ,client_Child_name , client_phone,client_national_id,pay_prise_of_subscription FROM Clients WHERE pay_prise_of_subscription = ?''',(1,))
                data = self.cur.fetchall()
            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row, form in enumerate(data):

                for column, forme in enumerate(form):
                    if column == 4:
                        if forme == 0:
                            aa = "Yes"
                            self.tableWidget.setItem(row, column, QTableWidgetItem(str(aa)))
                        else:
                            aa = "No"
                            self.tableWidget.setItem(row, column, QTableWidgetItem(str(aa)))
                    else:
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str(forme)))
                    column += 1

                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
        except Exception :
            self.null_error()
        else:
            self.lineEdit.setText("")

  ###############################################################################################################################################
    ########################import clients


    def EXport_clients(self):
        file = Export('clients')

        try :

            for i in range(self.tableWidget.rowCount() - 1 ) :
                file.add_data(1,  i + 1, self.tableWidget.item(i, 0).text())
                file.add_data(2,  i + 1, self.tableWidget.item(i, 1).text())
                file.add_data(3,  i + 1, self.tableWidget.item(i, 2).text())
                file.add_data(4,  i + 1, self.tableWidget.item(i, 3).text())
                file.add_data(5,  i + 1, self.tableWidget.item(i, 4).text())
                '''
                for j in range(5) :
                    file.add_data(i + 1, j + 1 ,self.tableWidget.item(i , j).text())
                    print(self.tableWidget.item(i , j).text())
                    print(i)
                    print(j)
                '''
            file.close_file()
            print("done")
        except Exception :
            file.close_file()
            print("error")
    ########################################################################################################################################"""
    ##############################user

    def add_user(self):
        user_name = self.lineEdit_11.text()
        user_password = self.lineEdit_12.text()
        user_phone = self.lineEdit_14.text()
        user_national_id = self.lineEdit_13.text()
        time_of_add_user = datetime.datetime.now()

        self.cur.execute('''INSERT INTO Users (user_name,user_password,user_national_id,user_phone,time_of_add_user) 
                    VALUES (?,?,?,?,?)''',(user_name,user_password,user_phone,user_national_id,time_of_add_user))

        self.db.commit()
        self.com()

    def seartch_edit_user(self):
        try :
            user_name = self.lineEdit_15.text()
            self.cur.execute('''SELECT user_password,user_national_id,user_phone FROM Users WHERE user_name = ? ''',(user_name,))
            data = self.cur.fetchone()
            self.lineEdit_17.setText(data[0])
            self.lineEdit_16.setText(data[1])
            self.lineEdit_18.setText(data[2])
        except Exception :
            self.null_error()
        else:
            self.groupBox_7.setEnabled(True)
            self.lineEdit_15.setText("")

    def edit_user(self):
        try :
            user_password = self.lineEdit_17.text()
            user_national_id = self.lineEdit_16.text()
            user_phone = self.lineEdit_18.text()
            self.cur.execute('''UPDATE Users SET user_password = ? ,user_national_id = ?,user_phone = ? WHERE user_national_id = ?''',(user_password,user_national_id,user_phone,user_national_id))
            self.db.commit()
        except Exception :
            self.null_error()
        else :
            self.lineEdit_17.setText("")
            self.lineEdit_16.setText("")
            self.lineEdit_18.setText("")
            self.groupBox_7.setEnabled(False)

    def delete_user(self):
        try :
            user_national_id = self.lineEdit_16.text()
            self.cur.execute('''DELETE FROM Users WHERE user_national_id = ?''',(user_national_id,))
            self.db.commit()
        except Exception :
            self.null_error()
        else :
            self.lineEdit_17.setText("")
            self.lineEdit_16.setText("")
            self.lineEdit_18.setText("")
            self.groupBox_7.setEnabled(False)

    def logout(self):
        self.db.close()
        self.close()
        self.login = login()
        self.login.show()

    ##################################################################################################################################################
    ######################historiq
    def com(self):
        self.comboBox_3.clear()
        self.cur.execute('''SELECT user_name FROM Users''')
        data = self.cur.fetchall()
        for i in data :
            self.comboBox_3.addItem(i[0])

    def show_all_historiq(self):
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        self.cur.execute('''SELECT user_id ,action , time FROM historiq''')
        data = self.cur.fetchall()
        self.cur.execute('''SELECT id,user_name FROM Users''')
        users = self.cur.fetchall()
        for row,form in enumerate(data):

            for column , forme in enumerate(form):
                if column == 0 :
                    #print(users[forme - 1][1])
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(users[forme - 1][1])))
                elif column == 1 :
                    if forme == 0 :
                        aa = "add cliest"
                        self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(aa)))
                    elif forme == 1:
                        aa = "edit client"
                        self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(aa)))
                    elif forme == 2 :
                        aa = "delete client"
                        self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(aa)))
                else :
                    self.tableWidget_2.setItem(row,column,QTableWidgetItem(str(forme)))
                column += 1

            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)

    def seartch_historiq(self):
        try :
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            user_name = self.comboBox_3.currentIndex()
            action = self.comboBox_2.currentIndex()
            self.cur.execute('''SELECT user_id ,action , time FROM historiq WHERE user_id = ? AND action = ? ''',(user_name+1,action))
            data = self.cur.fetchall()
            self.cur.execute('''SELECT id,user_name FROM Users''')
            users = self.cur.fetchall()
            for row, form in enumerate(data):
                for column, forme in enumerate(form):
                    if column == 0:
                        # print(users[forme - 1][1])
                        self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(users[forme - 1][1])))
                    elif column == 1:
                        if forme == 0:
                            aa = "add cliest"
                            self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(aa)))
                        elif forme == 1:
                            aa = "edit client"
                            self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(aa)))
                        elif forme == 2:
                            aa = "delete client"
                            self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(aa)))
                    else:
                        self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(forme)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)



        except Exception :
            self.null_error()

    def Export_hestory(self):
        file = Export('hestory')
        try :

            for i in range(self.tableWidget.rowCount() - 1 ) :
                file.add_data(1,  i + 1, self.tableWidget_2.item(i, 0).text())
                file.add_data(2,  i + 1, self.tableWidget_2.item(i, 1).text())
                file.add_data(3,  i + 1, self.tableWidget_2.item(i, 2).text())
            file.close_file()
            print("done")
        except Exception :
            file.close_file()
            print("error")
    ###########################################################################################################################################"
    #####################################login

class login(QMainWindow,LoginWin):
    def __init__(self,parent = None):
        super(login, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handling_button()
        self.db = sqlite3.connect('Data_base/data.db')
        self.cur = self.db.cursor()
    def handling_button(self):
        self.pushButton.clicked.connect(self.check_data)

    def check_data(self):
        user_name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        self.cur.execute('''SELECT id,user_name,user_password FROM Users''')
        data = self.cur.fetchall()
        for log in data :
            if user_name == log[1] and password == log[2] :
                global a_user_name
                a_user_name = log[0]
                self.main_window()

            #else:
             #   msg = QMessageBox()
              #  msg.setText("password incorect !")
               # msg.setWindowTitle("login")
                #msg.setIcon(QMessageBox.Warning)
                #x = msg.exec_()

    def main_window(self):
        self.db.close()
        self.close()
        self.ui = ui()
        self.ui.show()

def main():
    app = QApplication(argv)
    window = ui()
    #window = login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

