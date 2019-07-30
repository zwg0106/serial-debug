# -*- coding: utf-8 -*-

import time
import os
from PyQt5.QtCore import QDateTime, QTimer, QByteArray, QIODevice, QThread, pyqtSignal
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel, QFileDialog
from serial_debug import Ui_MainWindow as uiSerial
from serial_icon import SerialIcon

CURR_PATH = os.path.dirname(__file__)
SERIAL_STOP_BITS = {
    "1": "OneStop",
    "1.5": "OneAndHalfStop",
    "2": "TwoStop"
}

class Serial(QMainWindow, uiSerial):
    def __init__(self, parent=None):
        super(Serial, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("串口调试助手V1.0")
        self.setWindowIcon(SerialIcon().getQIcon())
        self.numSend = 0
        self.numRcv = 0
        self.timerSend = None
        self.ports = {}
        self.serial = QSerialPort()
        self.initTimerSend()
        self.setupSigSlot()
        self.setSerialStatusBar()
        self.setupThread()
        self.bytesWritten = 0

    def setupThread(self):
        """
        create port scan, receive and send threads
        """
        # port scan thread
        self.portScanThread = SerialPortScanThread()
        self.portScanThread.portScanSig.connect(self.getAvailSerialPorts)
        self.portScanThread.start()

        # receive thread
        self.rcvThread = RcvThread(self, self.serial)
        self.rcvThread.rcvSig.connect(self.setReceivedText)
        self.rcvThread.start()

    def setupSigSlot(self):
        self.pushButton_open_close.clicked.connect(self.openClosePort)
        self.pushButton_send.clicked.connect(self.sendTextData)
        self.pushButton_clean_send.clicked.connect(self.cleanSend)
        self.pushButton_clean_rcv.clicked.connect(self.cleanRcv)
        self.pushButton_sendfile.clicked.connect(self.sendFile)
        self.pushButton_openfile.clicked.connect(self.openFile)
        self.pushButton_save.clicked.connect(self.saveFile)
        self.checkBox_send_peroidically.stateChanged.connect(self.timerAutoSend)

    def initTimerSend(self):
        self.timerSend = QTimer(self)
        self.timerSend.timeout.connect(self.sendTextData)

    def getAvailSerialPorts(self, portList):
        """
        process available port list from signal
        """
        tmpPortNameL = []
        comingPortNameL = []
        if len(portList):
            for port in portList:
                comingPortNameL.append(port.portName())

        tmpPortNameL = list(self.ports.keys())

        if not len(comingPortNameL):
            self.statusbar.showMessage("无可用串口!", 5000)

        if len(tmpPortNameL) == len(comingPortNameL) and \
                set(tmpPortNameL) == set(comingPortNameL):
            return
        else:
            self.comboBox_port.clear()
            if len(portList):
                for port in portList:
                    self.ports[port.portName()] = port
                    self.comboBox_port.addItem(port.portName())
            else:
                self.ports = {}

    def setReceivedText(self, rcvTextList):
        """
        get serial receiving data then show in main window
        """
        _num = rcvTextList[0]
        self.numRcv += _num
        self.labelNumRcv.setText("接收:" + str(self.numRcv))

        _timeStamp = rcvTextList[1]
        if _timeStamp is not None:
            self.textBrowser_receive.append(_timeStamp)

        self.textBrowser_receive.insertPlainText("[RX]:")

        _data = rcvTextList[2]
        self.textBrowser_receive.insertPlainText(_data)

        self.textBrowser_receive.moveCursor(self.textBrowser_receive.textCursor().End)

    def setSerialStatusBar(self):
        """
        set serial status bar
        timestamp and rx&tx count
        """
        self.timer1S = QTimer(self)
        self.timer1S.timeout.connect(self.updateDateTime)
        self.labelDateTime = QLabel(self.statusbar)
        self.labelDateTime.setText(" " * 30)
        self.labelNumSend = QLabel(self.statusbar)
        self.labelNumRcv = QLabel(self.statusbar)
        self.labelNumSend.setText("发送:" + str(self.numSend))
        self.labelNumRcv.setText("接收:" + str(self.numRcv))
        self.statusbar.addPermanentWidget(self.labelNumSend, stretch=0)
        self.statusbar.addPermanentWidget(self.labelNumRcv, stretch=0)
        self.statusbar.addPermanentWidget(self.labelDateTime, stretch=0)
        self.timer1S.start(1)

    def updateDateTime(self):
        """
        update time
        """
        sysTime = QDateTime.currentDateTime().toString(" yyyy-MM-dd hh:mm:ss ")
        self.labelDateTime.setText(sysTime)

    def openClosePort(self):
        """
        open serial port and set attributes for opened ports
        or close serial port
        """
        if self.serial.isOpen():
            self.serial.close()
            self.statusbar.showMessage("关闭串口成功", 2000)
            self.pushButton_open_close.setText("打开串口")
            self.label_status.setProperty("isOn", False)
            self.label_status.style().polish(self.label_status)
            return

        if self.comboBox_port.currentText():
            # setup serial port
            port = self.ports[self.comboBox_port.currentText()]
            self.serial.setPort(port)
            self.serial.setBaudRate(getattr(QSerialPort, 'Baud' + self.comboBox_baud.currentText()))
            self.serial.setParity(getattr(QSerialPort, self.comboBox_partial.currentText() + 'Parity'))
            self.serial.setDataBits(getattr(QSerialPort, 'Data' + self.comboBox_data.currentText()))
            self.serial.setStopBits(getattr(QSerialPort, SERIAL_STOP_BITS[self.comboBox_stop.currentText()]))
            self.serial.setFlowControl(QSerialPort.NoFlowControl)

            isOK = self.serial.open(QIODevice.ReadWrite)
            if isOK:
                self.serial.clear()
                self.statusbar.showMessage("打开串口成功", 3000)
                self.pushButton_open_close.setText("关闭串口")
                self.label_status.setProperty("isOn", True)
                self.label_status.style().polish(self.label_status)
            else:
                QMessageBox.warning(self, "警告", "打开串口失败", QMessageBox.Yes)
                self.statusbar.showMessage("打开串口失败", 3000)
                self.pushButton_open_close.setText("打开串口")
                self.label_status.setProperty("isOn", False)
                self.label_status.style().polish(self.label_status)

    def sendTextData(self):
        """
        send data by serial port
        """
        if not self.serial.isOpen():
            self.statusbar.showMessage("串口未打开!", 5000)
            return

        _data = self.plainTextEdit_send.toPlainText()

        if not _data:
            self.statusbar.showMessage("没有发送数据!", 5000)
            return

        self.serial.write(QByteArray(_data.encode('utf-8')))

        self.numSend += len(_data)
        self.labelNumSend.setText("发送:" + str(self.numSend))

    def cleanSend(self):
        """
        clean send data in window
        """
        self.plainTextEdit_send.clear()
        self.numSend = 0
        self.labelNumSend.setText("发送:" + str(self.numSend))
        self.statusbar.showMessage("清除发送窗口", 1000)

    def cleanRcv(self):
        """
        clean receive data in window
        """
        self.textBrowser_receive.clear()
        self.numRcv = 0
        self.labelNumRcv.setText("接收:" + str(self.numRcv))
        self.statusbar.showMessage("清除接收窗口", 1000)

    def openFile(self):

        fileName, fileType = QFileDialog.getOpenFileName(self, "打开文件", CURR_PATH, "All files (*)")
        if fileName:
            oldText = self.plainTextEdit_send.toPlainText()
            try:
                with open(fileName, 'r', encoding='utf-8') as fl:
                    self.plainTextEdit_send.clear()
                    self.plainTextEdit_send.setPlainText(fl.read())
                    self.lineEdit_filename.setText(fileName)
            except:
                self.plainTextEdit_send.setPlainText(oldText)
                self.lineEdit_filename.clear()
                QMessageBox.warning(self, "警告", "解码失败", QMessageBox.Yes)
        else:
            self.statusbar.clearMessage()
            self.statusbar.showMessage("没有选择文件", 5000)

    def sendFile(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "打开文件", CURR_PATH, "All files (*)")
        if fileName:
            _data = None
            with open(fileName, 'rb') as fl:
                _data = fl.read()
            if not self.serial.isOpen():
                QMessageBox.warning(self, "警告", "串口未打开!", QMessageBox.Yes)
                return
            if not _data:
                QMessageBox.warning(self, "警告", "没有发送数据!", QMessageBox.Yes)
                return
            status, msg = self.sendThread.sendData(_data.decode('utf-8'))
            if status is False:
                QMessageBox.warning(self, "警告", msg, QMessageBox.Yes)
            else:
                self.numSend += int(msg)
                self.labelNumSend.setText("发送:" + str(self.numSend))

    def saveFile(self):
        """
        save data to file
        """
        fileName, fileType = QFileDialog.getSaveFileName(self, "打开文件", CURR_PATH, "All files (*)")
        if fileName:
            with open(fileName, 'w') as fl:
                strText = self.textBrowser_receive.toPlainText()
                if strText is not None:
                    strText = str(strText)
                    fl.write(strText)
        else:
            QMessageBox.warning(self, "警告", "无法打开文件！", QMessageBox.Yes)

    def timerAutoSend(self):
        """
        Auto send data by serial port
        """
        if self.checkBox_send_peroidically.checkState():
            time = self.lineEdit_timer_value.text()
            try:
                timeValue = int(time, 10)
            except:
                QMessageBox.warning(self, "警告", "请输入有效的定时时间!", QMessageBox.Yes)
                return None

            if timeValue <= 0:
                QMessageBox.warning(self, "警告", "定时时间必须大于0!", QMessageBox.Yes)
                return None
           #start timer
            self.timerSend.start(timeValue)
        else:
           #stop timer
           if self.timerSend.isActive():
               self.timerSend.stop()

    def closeEvent(self, event):
        """
        handle serial port close event
        """
        if self.timerSend.isActive():
            self.timerSend.stop()
        if self.timer1S.isActive():
            self.timer1S.stop()
        self.portScanThread.quit()
        self.rcvThread.quit()
        if self.serial.isOpen():
            self.serial.close()
        super(Serial, self).closeEvent(event)


class SerialPortScanThread(QThread):
    """
    thread to monitor available serial port
    """
    portScanSig = pyqtSignal(list)

    def __init__(self):
        super(SerialPortScanThread, self).__init__()

    def run(self):
        while True:
            ports = QSerialPortInfo.availablePorts()
            if not ports:
                self.portScanSig.emit([])
            else:
                self.portScanSig.emit(ports)
            time.sleep(2)

class RcvThread(QThread):
    """
    thread to get data from serial
    """
    # [num, timestamp, data]
    rcvSig = pyqtSignal(list)

    def __init__(self, obj, serial, parent=None):
        super(RcvThread, self).__init__(parent)
        self.__obj = obj
        self.__serial = serial

    def run(self):
        while True:
            if self.__serial.isOpen():
                num = self.__serial.bytesAvailable()
                if num:
                    _data = self.__serial.readAll()
                    _data = _data.data()

                    currTime = None
                    if self.__obj.checkBox_timestamp.isChecked():
                        currTime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
                        currTime = ("<span style='text-decoration:underline; color:green; font-size:12px;'>" + \
                                    "[" + currTime + "]" + "</span>")

                    if self.__obj.checkBox_display.isChecked():
                        out = ''
                        for i in range(0, len(_data)):
                            out = out + '0x{:02X}'.format(_data[i]) + ' '
                    else:
                        try:
                            out = _data.decode('utf-8')
                        except:
                            out = (r"<span style='text-decoration:underline; color:red; font-size:16px;'>" + \
                                   r"解码失败" + repr(_data) + r"</span>")

                    print([num, currTime, out])
                    self.rcvSig.emit([num, currTime, out])

                    time.sleep(0.01)
                else:
                    time.sleep(0.5)