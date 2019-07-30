# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from serial import Serial

if __name__ == "__main__":
    app = QApplication(sys.argv)
    serialMainWin = Serial()
    serialMainWin.show()
    sys.exit(app.exec_())