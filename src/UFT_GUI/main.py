#!/usr/bin/env python
# encoding: utf-8

'''
Created on Nov 01, 2014
@author: mzfa
'''
__author__ = "mzfa"
__version__ = "1.0"
__email__ = "mzfa@cypress.com"

import sys
sys.path.append("./src/")

import logging
import time
from PyQt4.QtGui import QApplication
from PyQt4 import QtGui, QtCore
from UFT_GUI.UFT_UiHandler import UFT_UiHandler
from UFT_GUI import log_handler

app = QApplication(sys.argv)
app.setStyle("Plastique")

try:
    import UFT
    from UFT.channel import Channel
except Exception as e:
    msg = QtGui.QMessageBox()
    msg.critical(msg, "error", e.message)
    # msg.exec_()


class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        # self.qtobj = QtCore.QObject()
        self.ui = UFT_UiHandler()
        self.ui.setupUi(self)
        self.ui.setupWidget(self)
        self.__setupSignal()

    def __setupSignal(self):
        """start_pushButton for log display test,
        to be changed as "start" function later
        """

        handler = log_handler.QtHandler()
        handler.setFormatter(UFT.formatter)
        UFT.logger.addHandler(handler)
        UFT.logger.setLevel(logging.INFO)
        log_handler.XStream.stdout().messageWritten.connect(
            self.ui.append_format_data)
        self.ui.start_pushButton.clicked.connect(self.start_click)
        self.ui.partNum_comboBox.currentIndexChanged.connect(
            self.ui.testItem_update)
        self.ui.revision_comboBox.currentIndexChanged.connect(
            self.ui.update_table)
        self.ui.submit_pushButton.clicked.connect(self.ui.submit_config)
        self.ui.search_lineEdit.returnPressed.connect(self.ui.search)
        self.ui.search_pushButton.clicked.connect(self.ui.search)
        self.ui.buttonGroup.buttonClicked.connect(self.ui.push_multi_mpls)
        self.ui.sn_lineEdit_1.textChanged.connect(self.ui.show_image)
        self.ui.sn_lineEdit_2.textChanged.connect(self.ui.show_image)
        self.ui.sn_lineEdit_3.textChanged.connect(self.ui.show_image)
        self.ui.sn_lineEdit_4.textChanged.connect(self.ui.show_image)
        self.ui.checkBox.toggled.connect(self.ui.config_edit_toggle)

        self.u = Update()

    def start_click(self):
        try:
            barcodes = self.ui.barcodes()
            cable_barcodes = self.ui.cabel_barcodes()
            self.u.loaddata(barcodes, cable_barcodes)
            self.connect(self.u, QtCore.SIGNAL('progress_bar'),
                         self.ui.progressBar.setValue)
            self.connect(self.u, QtCore.SIGNAL('is_alive'),
                         self.ui.auto_enable_disable_widgets)
            self.connect(self.u, QtCore.SIGNAL("dut_status"),
                         self.ui.set_status_text)
            self.connect(self.u, QtCore.SIGNAL('time_used'),
                         self.ui.print_time)
            self.u.start()

        except Exception as e:
            msg = QtGui.QMessageBox()
            msg.critical(self, "error", e.message)
            # msg.show()
            # msg.exec_()


class Update(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()

    def loaddata(self, barcodes, cable_barcodes):
        self.barcodes = barcodes
        self.cable_barcodes = cable_barcodes

    def run(self):
        sec_count = 0
        ch = Channel(barcode_list=self.barcodes, cable_barcodes_list=self.cable_barcodes, channel_id=0,
                          name="UFT_CHANNEL")

        ch.auto_test()
        self.emit(QtCore.SIGNAL("is_alive"), 1)
        while ch.isAlive():
            sec_count += 1
            self.emit(QtCore.SIGNAL("progress_bar"), ch.progressbar)
            self.emit(QtCore.SIGNAL("time_used"), sec_count)
            for dut in ch.dut_list:
                if dut is not None:
                    self.emit(QtCore.SIGNAL("dut_status"), dut.slotnum,
                              dut.status)
            time.sleep(1)

        self.emit(QtCore.SIGNAL("progress_bar"), 100)
        for dut in ch.dut_list:
            if dut is not None:
                self.emit(QtCore.SIGNAL("dut_status"), dut.slotnum, dut.status)

        ch.save_db()

        time.sleep(1)
        del ch
        self.emit(QtCore.SIGNAL("is_alive"), 0)


def main():
    # app = QApplication(sys.argv)
    # app.setStyle("Plastique")
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
