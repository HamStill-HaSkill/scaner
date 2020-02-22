from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from scaner import *
import scapy.all as sc
import sys


def scaner(ip, time):
    IPlist = list()
    arpReqBroad = sc.Ether(dst="ff:ff:ff:ff:ff:ff")/sc.ARP(pdst=ip)
    answer = sc.srp(arpReqBroad, timeout=time, verbose=False)[0]
    # print(sc.srp(arpReqBroad, timeout=1)[1].summary())
    if len(answer) == 0:
        return IPlist
    for elem in answer:
        IPlist.append({'ip': elem[1].psrc, 'mac': elem[1].hwsrc})
    IPlist.append({'ip': elem[1].pdst, 'mac': elem[1].hwdst})
    return IPlist


class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.runBtn.clicked.connect(self.scan)


    def scan(self):
        # self.ui.ipLine.text().split('.')
        self.ui.tableWidget.clear()
        ips = self.ui.ipLine.text().split('.')
        masks = self.ui.maskLine.text().split('.')
        if self.ui.maskLine.text() == '255.255.255.0':
            ResList = scaner(self.ui.ipLine.text() + '/24', 1)
        else:
            ips = [int(item) for item in ips]
            origMasks = [int(item) for item in masks]
            masks = [int(item) for item in masks]
            ResList = list()
            option = list()
            for i in range(4):
                while masks[i] < 255:
                    currentIp = ips[:i] + masks[i:]
                    option.append('.'.join(map(str, currentIp)))
                    masks[i] += 1
                    if (i+1 != 4) and masks[i] == 255:
                        if (masks[i+1] < 255):
                            masks[i+1] += 1
                            masks[i] = origMasks[i]
            if option != []:
                ResList.append(scaner(option, 0.1))
                ResList = ResList[0]
        print(ResList)
        if (len(ResList) == 0):
            ResList = [{'ip': 'Not fond', 'mac':'Not fond'}]
        self.ui.tableWidget.setColumnCount(2)
        self.ui.tableWidget.setRowCount(len(ResList)+1)
        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem("IP"))
        self.ui.tableWidget.setItem(0, 1, QTableWidgetItem("MAC"))
        row = 0
        for item in ResList:
            row += 1
            column = 0
            self.ui.tableWidget.setItem(row, column, QTableWidgetItem(item['ip']))
            column += 1
            self.ui.tableWidget.setItem(row, column, QTableWidgetItem(item['mac']))




if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
