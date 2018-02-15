import os
import sys
import requests
import pyqtgraph as pg
import simplejson as json

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from fake_useragent import UserAgent


no_of_stocks = 0
all_stock = ['1', '2', '3', '4', '5', '6', '7', '8', '10', '11', '12', '14', '15', '16', '17', '18', '19', '20', '22', '23', '25', '26', '27', '29', '30', '31', '32', '34', '35', '36', '38', '39', '40', '41', '42', '44', '45', '46', '50', '51', '52', '53', '54', '55', '56', '57', '58', '61', '62', '63', '64', '65', '66', '68', '69', '70', '71', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '86', '87', '89', '92', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '107', '109', '110', '112', '113', '114', '116', '117', '118', '119', '120', '121', '122', '123', '124', '127', '128', '129', '130', '131', '132', '133', '135', '136', '138', '139', '142', '144', '146', '147', '148', '149', '151', '152', '154', '156', '158', '163', '165', '166', '167', '168', '169', '171', '173', '174', '175', '176', '177', '178', '179', '182', '183', '186', '188', '189', '190', '194', '196', '198', '200', '201', '202', '204', '205', '207', '211', '213', '215', '218', '220', '221', '222', '223', '224', '226', '227', '228', '230', '231', '232', '236', '237', '238', '239', '242', '243', '244', '245', '247', '248', '250', '251', '252', '255', '257', '258', '260', '261', '263', '264', '267', '268', '269', '270', '271', '272', '273', '274', '275', '276', '278', '279', '280', '282', '285', '286', '287', '288', '289', '291', '293', '296', '297', '298', '299', '300', '303', '306', '308', '309', '310', '311', '313', '315', '316', '317', '318', '320', '321', '322', '323', '326', '327', '328', '329', '330', '332', '333', '334', '337', '338', '340', '341', '342', '343', '345', '346', '347', '348', '352', '357', '358', '359', '361', '363', '365', '368', '369', '372', '373', '376', '377', '378', '382', '383', '386', '387', '388', '389', '390', '391', '392', '393', '395', '402', '403', '404', '405', '406', '408', '410', '411', '416', '418', '419', '420', '422', '423', '425', '431', '435', '439', '440', '450', '464', '475', '480', '482', '483', '486', '488', '489', '491', '493', '494', '496', '498', '500', '505', '506', '508', '511', '513', '515', '517', '518', '521', '524', '525', '527', '532', '533', '535', '536', '538', '543', '544', '546', '547', '548', '550', '551', '552', '553', '555', '558', '559', '560', '567', '568', '569', '570', '573', '575', '576', '579', '581', '583', '585', '588', '589', '590', '592', '593', '595', '598', '599', '601', '603', '604', '605', '606', '607', '608', '609', '610', '611', '612', '613', '616', '617', '618', '619', '620', '621', '622', '626', '627', '628', '629', '630', '632', '636', '637', '638', '641', '643', '645', '646', '647', '648', '650', '651', '653', '655', '656', '657', '658', '659', '660', '661', '663', '665', '666', '668', '669', '670', '673', '674', '675', '677', '678', '680', '681', '682', '683', '684', '685', '686', '687', '688', '690', '692', '693', '694', '696', '697', '698', '699', '700', '701', '702', '703', '706', '708', '709', '710', '715', '716', '717', '722', '723', '725', '727', '728', '729', '731', '732', '733', '735', '736', '737', '738', '746', '751', '752', '753', '754', '757', '759', '760', '762', '763', '769', '771', '775', '778', '800', '801', '802', '805', '806', '809', '813', '817', '818', '819', '820', '822', '823', '825', '826', '831', '833', '835', '836', '838', '839', '840', '841', '845', '847', '848', '850', '852', '855', '856', '857', '858', '859', '861', '862', '867', '868', '869', '874', '878', '881', '882', '883', '885', '887', '888', '894', '896', '897', '900', '901', '902', '903', '904', '906', '907', '910', '912', '913', '914', '915', '916', '918', '919', '921', '926', '927', '929', '931', '938', '939', '941', '943', '945', '952', '966', '968', '969', '970', '973', '978', '980', '981', '983', '985', '987', '988', '989', '990', '991', '992', '993', '995', '996', '998', '999', '1001', '1002', '1003', '1004', '1010', '1013', '1019', '1029', '1030', '1033', '1036', '1037', '1038', '1043', '1044', '1045', '1046', '1047', '1049', '1050', '1052', '1053', '1055', '1059', '1062', '1063', '1064', '1065', '1068', '1070', '1071', '1072', '1083', '1088', '1093', '1094', '1097', '1098', '1099', '1100', '1105', '1108', '1109', '1111', '1114', '1118', '1123', '1124', '1126', '1128', '1129', '1132', '1133', '1135', '1137', '1138', '1142', '1145', '1150', '1157', '1160', '1161', '1166', '1168', '1169', '1170', '1171', '1172', '1173', '1178', '1180', '1185', '1186', '1189', '1191', '1192', '1193', '1194', '1198', '1199', '1200', '1201', '1202', '1203', '1205', '1208', '1211', '1212', '1215', '1217', '1218', '1220', '1221', '1222', '1224', '1225', '1226', '1227', '1229', '1232', '1233', '1234', '1235', '1236', '1237', '1238', '1239', '1240', '1241', '1243', '1245', '1246', '1247', '1249', '1250', '1251', '1252', '1253', '1255', '1258', '1259', '1260', '1262', '1263', '1265', '1266', '1268', '1269', '1270', '1271', '1272', '1273', '1275', '1278', '1288', '1299', '1313', '1316', '1333', '1336', '1338', '1339', '1359', '1361', '1368', '1383', '1388', '1389', '1393', '1398', '1618', '1700', '1708', '1766', '1776', '1777', '1786', '1800', '1808', '1812', '1813', '1818', '1822', '1828', '1838', '1862', '1868', '1881', '1882', '1883', '1886', '1888', '1889', '1893', '1898', '1899', '1910', '1913', '1918', '1919', '1928', '1929', '1958', '1963', '1972', '1988', '1997', '2000', '2002', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2018', '2020', '2028', '2038', '2039', '2088', '2099', '2196', '2200', '2208', '2222', '2238', '2266', '2282', '2300', '2307', '2309', '2314', '2318', '2319', '2320', '2322', '2323', '2326', '2328', '2330', '2331', '2333', '2337', '2338', '2339', '2340', '2341', '2342', '2343', '2345', '2348', '2349', '2355', '2356', '2368', '2371', '2378', '2379', '2380', '2382', '2383', '2388', '2398', '2600', '2601', '2607', '2628', '2633', '2662', '2668', '2678', '2688', '2689', '2700', '2722', '2727', '2728', '2777', '2778', '2788', '2789', '2800', '2801', '2819', '2821', '2822', '2823', '2828', '2832', '2836', '2838', '2866', '2868', '2877', '2878', '2880', '2882', '2883', '2888', '2898', '2899', '3300', '3303', '3308', '3311', '3313', '3318', '3323', '3328', '3330', '3331', '3333', '3337', '3339', '3344', '3355', '3360', '3368', '3377', '3378', '3382', '3383', '3398', '3399', '3618', '3683', '3688', '3788', '3800', '3808', '3813', '3818', '3833', '3838', '3883', '3886', '3888', '3889', '3898', '3899', '3900', '3918', '3933', '3948', '3958', '3968', '3983', '3988', '3989', '3993', '3998', '3999', '4333', '4335', '4338', '6030', '6066', '6138', '6288', '6388', '6808', '6818', '6823', '6837', '6880', '6881', '6882', '8095']
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


def one_month_crawl(number):
    ua = UserAgent()
    header = {'User-Agent': str(ua.random)}
    proxy = {'https':'113.76.96.143:9797'}
    url = 'http://money18.on.cc/chartdata/m1/price/' + number + '_price_m1.txt'
    request = requests.get(url, headers=header, proxies=proxy)
    jsonarray = json.loads(request.text)

    global temp
    temp = []
    labels = jsonarray['x_axis']['labels']
    for item in labels:
        extract = item[4:]
        if extract[0] == '0':
            if extract[2] == '0':
                temp.append(extract[1] + '/' + extract[3])
            else:
                temp.append(extract[1] + '/' + extract[2:])
        else:
            if extract[2] == '0':
                temp.append(extract[0:1] + '/' + extract[3])
            else:
                temp.append(extract[0:1] + '/' + extract[2:3])

    high = jsonarray['high']['values']
    low = jsonarray['low']['values']
    stock_open = jsonarray['open']['values']
    close = jsonarray['price']['values']
    timestamp = []
    for tick in range(len(high)):
        timestamp.append(tick)

    data = zip(timestamp, stock_open, close, low, high)
    return data

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


class CandleStickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QPicture()
        p = QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = (self.data[1][0] - self.data[0][0]) / 3.

        for (t, open, close, min, max) in self.data:
            p.drawLine(QPointF(t, min), QPointF(t, max))
            if open > close:
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setBrush(pg.mkBrush('g'))
            p.drawRect(QRectF(t - w, open, w * 2, close - open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QRectF(self.picture.boundingRect())


class Window(object):
    def initUI(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1080, 900)
        Dialog.setWindowTitle('HK Stocks Monitoring Software 1.7 by Nighost')

        stylesheet = "::section{background-color:black; color:white; font-weight: bold}"

        self.tab = QTabWidget(Dialog)
        self.tab.setGeometry(QRect(30, 570, 900, 300))
        self.tab.addTab(QWidget(), QString('1-Day'))
        self.tab.addTab(QWidget(), QString('1-Month'))

        self.updatelabel = QLabel(Dialog)
        self.updatelabel.setGeometry(QRect(700, 555, 250, 30))
        self.updatelabel.setObjectName(_fromUtf8("updatelabel"))

        self.table = QTableWidget(Dialog)
        self.table.setGeometry(QRect(30, 50, 900, 500))
        self.table.setObjectName(_fromUtf8("tableWidget"))
        self.table.setColumnCount(9)
        update_url()
        self.table.setRowCount(no_of_stocks)
        self.table.setHorizontalHeaderLabels(['Current', 'Up/Down', 'Change %', 'D High', 'D Low', 'M High', 'M Low', '52W High',
                                                    '52W Low'])
        self.table.setVerticalHeaderLabels(stock_number)
        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStyleSheet(stylesheet)
        self.table.cellClicked.connect(lambda:self.updateChart(self.table, self.tab))
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

        self.label2 = QLabel(Dialog)
        self.label2.setGeometry(QRect(950, 260, 121, 20))
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.label2.setText(_translate("Dialog", "Percentage from 52W :", None))

        self.lineEdit2 = QLineEdit(Dialog)
        self.lineEdit2.setGeometry(QRect(950, 280, 113, 31))
        self.lineEdit2.setObjectName(_fromUtf8("lineEdit_2"))

        self.downloadBtn = QPushButton(Dialog)
        self.downloadBtn.setGeometry(QRect(970, 320, 75, 23))
        self.downloadBtn.setObjectName(_fromUtf8("pushButton3"))
        self.downloadBtn.setText(_translate("Dialog", "Download", None))
        self.downloadBtn.clicked.connect(lambda: self.downloadStock(self.lineEdit2))

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

    def downloadStock(self, lineEdit2):
        text = lineEdit2.text()
        start_urls = []
        location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        f = open(os.path.join(location, '52WFilter.csv'), 'w')

        for number in all_stock:
            while len(number) < 5:
                number = '0' + number
            start_urls.append('http://money18.on.cc/js/daily/hk/quote/' + number.strip() + '_d.js')
            start_urls.append('http://money18.on.cc/js/real/hk/quote/' + number.strip() + '_r.js')

        for stock in all_stock:
            data = crawl_stock(start_urls[0])
            print start_urls[0]
            fiftyTwoLow = options[4](data)
            name = options[0](data)
            start_urls.pop(0)
            data = crawl_stock(start_urls[0])
            currPrice = options[6](data)
            range = (float(currPrice) - float(fiftyTwoLow)) / float(fiftyTwoLow) * 100
            if range <= float(text):
                f.write(name + ',' + currPrice + ',' + fiftyTwoLow + ',' + str(range) + '%\n')
            start_urls.pop(0)

        f.close()

    def updateChart(self, table, tab):
        number = table.verticalHeaderItem(table.currentRow()).text()
        while len(number) < 5:
            number = '0' + number
        item = CandleStickItem(one_month_crawl(number))
        ticks = [list(zip(range(len(temp)), temp))]

        plot = pg.PlotWidget()
        x_axis = plot.getAxis('bottom')
        x_axis.setTicks(ticks)
        plot.plot()
        plot.addItem(item)

        tab.clear()
        tab.addTab(QWidget(), QString('1-Day'))
        tab.addTab(plot, QString('1-Month'))

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
        layout = msg.layout()
        horizontalSpacer = QSpacerItem(500, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(horizontalSpacer, layout.rowCount(), 0, 1, layout.columnCount())

        msg.setIcon(QMessageBox.Information)
        msg.setText('Current Version : 1.7\n\nVersion Highlight :\n\n' +
                    '- Chart Data for 1 month Established\n')
        msg.setDetailedText('Previous Version Highlight :\n' +
                            'v1.6\n- Download 52-Week stock data function finished\n' +
                            'v1.5\n- Delete stock from monitoring table function finished\n' + '- Added Menubar (About Column)\n' +
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