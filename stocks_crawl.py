import os
import sys
import requests
import simplejson as json

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from fake_useragent import UserAgent


no_of_stocks = 0
stock_number = []
start_urls = []
crawltime = ''


try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


def crawl_stock(url):
    ua = UserAgent()
    header = {'User-Agent': str(ua.random)}
    proxy = {'https': '113.76.96.143:9797'}
    request = requests.get(url, headers=header, proxies=proxy)
    jsonarray = json.loads(json.dumps(request.text[request.text.find('{'):]))
    return jsonarray


def update_url():
    global no_of_stocks, stock_number, start_urls
    no_of_stocks = 0
    stock_number = []
    start_urls = []
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(location, 'stock-number'))
    for number in f.read().splitlines():
        no_of_stocks = no_of_stocks + 1
        stock_number.append(number)
        while len(number) < 5:
            number = '0' + number
        start_urls.append('http://money18.on.cc/js/daily/hk/quote/' + number.strip() + '_d.js')
        start_urls.append('http://money18.on.cc/js/real/hk/quote/' + number.strip() + '_r.js')
    f.close()


def insert_data(table, updatelabel):
    global start_urls, crawltime
    crawltime = ''
    for number in range(no_of_stocks):
        data = crawl_stock(start_urls[0])
        table.setItem(number, 5, QTableWidgetItem(options[1](data)))
        table.setItem(number, 6, QTableWidgetItem(options[2](data)))
        table.setItem(number, 7, QTableWidgetItem(options[3](data)))
        table.setItem(number, 8, QTableWidgetItem(options[4](data)))

        pp = options[5](data)
        start_urls.pop(0)
        data = crawl_stock(start_urls[0])
        cp = options[6](data)
        change = float(cp) - float(pp)
        percentage = change / float(pp) * 100
        table.setItem(number, 0, QTableWidgetItem(cp))
        table.setItem(number, 1, QTableWidgetItem(str(change)))
        if change < 0:
            table.item(number, 1).setBackground(QColor(255, 0, 0))
            table.item(number, 1).setTextColor(QColor(255, 255, 255))
        else:
            table.item(number, 1).setBackground(QColor(0, 255, 0))
        table.setItem(number, 2, QTableWidgetItem('%.2f' % percentage + '%'))
        table.setItem(number, 3, QTableWidgetItem(options[7](data)))
        table.setItem(number, 4, QTableWidgetItem(options[8](data)))
        start_urls.pop(0)

        if crawltime == '':
            crawltime = options[9](data)
            updatelabel.setText(_translate("Dialog", 'Last Update: ' + crawltime, None))
            updatelabel.setFont(QFont("Roman times", 10, QFont.Bold))

        for i in range(9):
            table.item(number, i).setTextAlignment(Qt.AlignCenter)


def stock_name(data):
    start = data.find('name') + 7
    end = data.find(',', start) - 1

    return data[start:end].encode('utf-8')


def previous_price(data):
    start = data.find('preCPrice') + 12
    print start
    end = data.find(',', start) - 1

    return data[start:end].encode('utf-8')


def current_price(data):
    start = data.find('np') + 6
    end = data.find(',', start) - 1

    return data[start:end].encode('utf-8')


def day_high(data):
    start = data.find('dyh') + 7
    end = data.find(',', start) - 1

    return data[start:end].encode('utf-8')


def day_low(data):
    start = data.find('dyl') + 7
    end = data.find('\'', start) - 1

    return data[start:end].encode('utf-8')


def month_high(data):
    start = data.find('mthHigh') + 10
    end = data.find(',', start) - 1

    return data[start:end].encode('utf-8')


def month_low(data):
    start = data.find('mthLow') + 9
    end = data.find(',', start) - 1

    return data[start:end].encode('utf-8')


def fifty_two_high(data):
    start = data.find('wk52High') + 11
    end = data.find(',', start) - 1

    return data[start:end].encode('utf-8')


def fifty_two_low(data):
    start = data.find('wk52Low') + 10
    end = data.find(',', start) - 1

    return data[start:end].encode('utf-8')


def crawl_time(data):
    start = data.find('ltt') + 7
    end = data.find(',', start) - 1

    return data[start:end].encode('utf-8')


options = { 0: stock_name,
            1: month_high,
            2: month_low,
            3: fifty_two_high,
            4: fifty_two_low,
            5: previous_price,
            6: current_price,
            7: day_high,
            8: day_low,
            9: crawl_time}


class Window(object):
    def initUI(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1080, 720)
        Dialog.setWindowTitle('HK Stocks Monitoring Software 1.5 by Nighost')

        stylesheet = "::section{background-color:black; color:white; font-weight: bold}"

        self.updatelabel = QLabel(Dialog)
        self.updatelabel.setGeometry(QRect(825, 670, 250, 30))
        self.updatelabel.setObjectName(_fromUtf8("updatelabel"))

        self.table = QTableWidget(Dialog)
        self.table.setGeometry(QRect(30, 50, 900, 600))
        self.table.setObjectName(_fromUtf8("tableWidget"))
        self.table.setColumnCount(9)
        update_url()
        self.table.setRowCount(no_of_stocks)
        self.table.setHorizontalHeaderLabels(['Current', 'Up/Down', 'Change %', 'D High', 'D Low', 'M High', 'M Low', '52W High',
                                                    '52W Low'])
        self.table.setVerticalHeaderLabels(stock_number)
        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStyleSheet(stylesheet)
        insert_data(self.table, self.updatelabel)

        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(950, 110, 111, 20))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label.setText(_translate("Dialog", "Enter Stock Number :", None))

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setGeometry(QRect(950, 130, 113, 31))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))

        self.addBtn = QPushButton(Dialog)
        self.addBtn.setGeometry(QRect(970, 170, 75, 23))
        self.addBtn.setObjectName(_fromUtf8("pushButton"))
        self.addBtn.setText(_translate("Dialog", "Add", None))
        self.addBtn.clicked.connect(lambda:self.addStock(self.table, self.lineEdit, self.updatelabel))

        self.deleteBtn = QPushButton(Dialog)
        self.deleteBtn.setGeometry(QRect(970, 200, 75, 23))
        self.deleteBtn.setObjectName(_fromUtf8("pushButton2"))
        self.deleteBtn.setText(_translate("Dialog", "Delete", None))
        self.deleteBtn.clicked.connect(lambda: self.deleteStock(self.table, self.lineEdit, self.updatelabel))

        aboutAction = QAction('About Purpose', Dialog)
        aboutAction.setShortcut('A')
        aboutAction.triggered.connect(lambda:self.purpose_dialog())

        versionAction = QAction('Version Log', Dialog)
        versionAction.setShortcut('V')
        versionAction.triggered.connect(lambda:self.version_log())

        self.menubar = QMenuBar(Dialog)
        about = self.menubar.addMenu('About')
        about.addAction(aboutAction)
        about.addAction(versionAction)

        self.timer = QTimer(Dialog)
        self.timer.timeout.connect(lambda:self.refresh(self.table, self.updatelabel))
        self.timer.start(60000)

        QMetaObject.connectSlotsByName(Dialog)

    def addStock(self, table, lineEdit, updatelabel):
        text = lineEdit.text()
        check = False
        for stock in stock_number:
            if text == stock:
                check = True
                break

        if check:
            lineEdit.clear()
        else:
            location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            f = open(os.path.join(location, 'stock-number'), 'w')
            stock_number.append(str(text))
            stock_number.sort(key=int)
            for number in stock_number:
                f.write('%s\n' % number)
            f.close()

            update_url()
            table.setRowCount(no_of_stocks)
            table.setVerticalHeaderLabels(stock_number)
            insert_data(table, updatelabel)
            lineEdit.clear()

    def deleteStock(self, table, lineEdit, updatelabel):
        text = lineEdit.text()
        check = False
        for stock in stock_number:
            if text == stock:
                stock_number.remove(text)
                check = True
                break

        if check:
            location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            f = open(os.path.join(location, 'stock-number'), 'w')
            stock_number.sort(key=int)
            for number in stock_number:
                f.write('%s\n' % number)
            f.close()

            update_url()
            table.setRowCount(no_of_stocks)
            table.setVerticalHeaderLabels(stock_number)
            insert_data(table, updatelabel)
            lineEdit.clear()
        else:
            lineEdit.clear()


    def refresh(self, table, updatelabel):
        update_url()
        table.setRowCount(no_of_stocks)
        table.setVerticalHeaderLabels(stock_number)
        insert_data(table, updatelabel)

    def purpose_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("This software is for educational purpose. It is not supposed to be used for commercial activity.")
        msg.setWindowTitle("About Purpose of this Software")
        msg.exec_()

    def version_log(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('\tCurrent Version : 1.5\n\n\tVersion Highlight :\n\n' +
                    '\t- Delete stock from monitoring table function finished\t\t\t\n')
        msg.setDetailedText('Previous Version Highlight :\n' +
                            'v1.4\n- UI modification\n- Added menu bar\n' +
                            'v1.3\n- Add stock to monitoring table function finished\n' +
                            '- Per minute auto-update of stock price\n- Colored cell to indicate up/down of stock' +
                            '- Last update time display\n' +
                            'v1.0 - v1.2\n- Basic framework of software\n- Setup crawl function')
        msg.setWindowTitle("Version Log of this Software")
        msg.exec_()


def main():
    app = QApplication(sys.argv)
    dialog = QDialog()
    ui = Window()
    ui.initUI(dialog)
    dialog.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()