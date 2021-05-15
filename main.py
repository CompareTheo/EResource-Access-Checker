from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from accessui import Ui_MainWindow
from vendors import available
import sys
import csv
import time


class CloneThread(QThread):
    countChanged = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        i = 0
        with open(checkfile, 'r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")
            givenurl = []
            expectedtitle = []

            with open('results.csv', 'w', newline='', encoding='utf-8') as savefile:
                for row in readCSV:
                    givenurl = row[0]
                    expectedtitle = row[1]

                    fireFoxOptions = webdriver.FirefoxOptions()
                    fireFoxOptions.headless = False
                    browser = webdriver.Firefox(options=fireFoxOptions)
                    try:
                        browser.get(givenurl)
                        time.sleep(5)
                        accesscheck = browser.find_element_by_xpath(user_count_query)
                        titlecheck = browser.find_element_by_xpath(proper_title_query)
                        titlestatus = titlecheck.text
                        accessstatus = accesscheck.txt
                        print(titlecheck.text, accesscheck.text)
                        browser.close()
                        time.sleep(2)
                        i = i + 1
                        self.countChanged.emit(i)
                    except NoSuchElementException:
                        titlestatus = "Error"
                        accessstatus = "Access not confirmed"
                        browser.close()
                        time.sleep(2)
                        i = i + 1
                        self.countChanged.emit(i)

                    resultsout = [givenurl, expectedtitle, accessstatus, titlestatus]
                    writer = csv.writer(savefile, delimiter=',')
                    writer.writerow(resultsout)


# GUI & Instruction Class
class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        Signal = QtCore.pyqtSignal
        super(ExampleApp, self).__init__(parent)
        self.running_thread = CloneThread()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_file)
        self.pushButton_2.clicked.connect(self.run_script)
        self.comboBox.addItems(available)
        self.comboBox.currentIndexChanged.connect(self.setingQueryStrings)
        self.running_thread.countChanged.connect(self.updateProgressBar)

    def get_file(self):
        global checkfile
        global record_count
        checkfile, _ = QFileDialog.getOpenFileName(None, 'Open File', r"", '')
        with open(checkfile, 'rb') as count:
            record_count = sum(1 for row in count)
            self.progressBar.setMaximum(record_count)
            print(record_count)
            count.close()

    def run_script(self):
        # self.pushButton.setEnabled(False)  # Disables the pushButton
        # self.startButton.setEnabled(False)
        self.running_thread.start()  # Finally starts the thread

    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

    def setingQueryStrings(self):
        global user_count_query
        global proper_title_query
        chosen_vendor = self.comboBox.currentText()
        with open('queries.csv') as f:
            for l, i in enumerate(f):
                available = i.split(',')
                if available[0] == chosen_vendor:
                    user_count_query = available[1]
                    proper_title_query = available[2]


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
