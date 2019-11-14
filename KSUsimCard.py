#coding=utf-8

import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
import re
import datetime
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from UsimCardUI import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.util import toHexString, toBytes

# add by dongfeng

imsi_pattern = r'12345

# add end


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "KSUsimWriter"))
        self.actionLoadCommandFile.triggered.connect(self.loadCommandFile)
        self.actionLoadIMSIFile.triggered.connect(self.loadIMSIFile)
        self.actionSingle_IMSI.triggered.connect(self.doSingleIMSI)
        self.actionBatch_IMSI.triggered.connect(self.doBatchIMSI)
        self.actionReadCard.triggered.connect(self.readCard)
        self.actionWriteCard.triggered.connect(self.writeCard)
        self.actionAbout.triggered.connect(self.doAbout)
        self.actionExit.triggered.connect(self.doExit)

        regex_IMSI_start = QRegExp("[0-9]{15}")
        validator_IMSI_start = QRegExpValidator(regex_IMSI_start, self.lineEdit_IMSI_start)
        self.lineEdit_IMSI_start.setValidator(validator_IMSI_start)
        self.lineEdit_IMSI_start.textChanged.connect(self.textChanged_IMSI_start)

        regex_KEY = QRegExp("([0-9]|[A-F]|[a-f]){32}")
        validator_KEY = QRegExpValidator(regex_KEY, self.lineEdit_KEY)
        self.lineEdit_KEY.setValidator(validator_KEY)
        self.lineEdit_KEY.textChanged.connect(self.textChanged_KEY)

        regex_OPC = QRegExp("([0-9]|[A-F]|[a-f]){32}")
        validator_OPC = QRegExpValidator(regex_OPC, self.lineEdit_OPC)
        self.lineEdit_OPC.setValidator(validator_OPC)
        self.lineEdit_OPC.textChanged.connect(self.textChanged_OPC)

        regex_HPLMN = QRegExp("[0-9]{5}([0-9]|F)")
        validator_HPLMN = QRegExpValidator(regex_HPLMN, self.lineEdit_HPLMN)
        self.lineEdit_HPLMN.setValidator(validator_HPLMN)
        self.lineEdit_HPLMN.textChanged.connect(self.textChanged_HPLMN)

        regex_FPLMN = QRegExp("([0-9]{5}([0-9]|F) ){3}([0-9]{5}([0-9]|F))")
        validator_FPLMN = QRegExpValidator(regex_FPLMN, self.lineEdit_FPLMN)
        self.lineEdit_FPLMN.setValidator(validator_FPLMN)
        self.lineEdit_FPLMN.textChanged.connect(self.textChanged_FPLMN)

        regex_SPN = QRegExp("([0-9]|[a-z]|[A-Z]|-|_){16}")
        validator_SPN = QRegExpValidator(regex_SPN, self.lineEdit_SPN)
        self.lineEdit_SPN.setValidator(validator_SPN)
        self.lineEdit_SPN.textChanged.connect(self.textChanged_SPN)

        self.param_map = {
            "HPLMN": [self.lineEdit_HPLMN, ""],
            "FPLMN": [self.lineEdit_FPLMN, ""],
            "IMSI_start": [self.lineEdit_IMSI_start, ""],
            "IMSI_done": [self.lineEdit_IMSI_done, "0"],
            "KEY": [self.lineEdit_KEY, ""],
            "OPC": [self.lineEdit_OPC, ""],
            "SPN": [self.lineEdit_SPN, ""],
        }
        self.cmds = []
        self.imsis = []
        self.batch_mode = True
        if self.batch_mode:
            self.doBatchIMSI()
        else:
            self.doSingleIMSI()
        sys.stdout = MyBrower(self.textBrowser_Log)
        return

    def textChanged_IMSI_start(self):
        if self.reset_inprogress:
            return;
        if self.batch_mode:
            self.lineEdit_IMSI_start.setText(self.param_map["IMSI_start"][1])
        else:
            res = self.setParamMap()
            if res != 0:
                self.lineEdit_IMSI_start.setText("")
        return
    def textChanged_KEY(self):
        if self.reset_inprogress:
            return;
        if self.batch_mode:
            self.lineEdit_KEY.setText(self.param_map["KEY"][1])
        else:
            res = self.setParamMap()
            if res != 0:
                self.lineEdit_KEY.setText("")
        return
    def textChanged_OPC(self):
        if self.reset_inprogress:
            return;
        if self.batch_mode:
            self.lineEdit_OPC.setText(self.param_map["OPC"][1])
        else:
            res = self.setParamMap()
            if res != 0:
                self.lineEdit_OPC.setText("")
        return
    def textChanged_HPLMN(self):
        if self.reset_inprogress:
            return;
        res = self.setParamMap()
        if res != 0:
            self.lineEdit_HPLMN.setText("")
        return
    def textChanged_FPLMN(self):
        if self.reset_inprogress:
            return;
        res = self.setParamMap()
        if res != 0:
            self.lineEdit_FPLMN.setText("")
        return
    def textChanged_SPN(self):
        if self.reset_inprogress:
            return;
        res = self.setParamMap()
        if res != 0:
            self.lineEdit_SPN.setText("")
        return

    def reset(self):
        self.reset_inprogress = True
        self.cmds = []
        self.imsis = []
        self.textBrowser_Command.setText(self.cmdsToText())
        self.textBrowser_IMSI.setText(self.imsisToText())
        for k in self.param_map:
            if k == "IMSI_done":
                self.param_map[k][1] = "0"
            else:
                self.param_map[k][1] = ""
            self.param_map[k][0].setText(self.param_map[k][1])
        self.reset_inprogress = False
        return

    def setParamMap(self):
        if self.batch_mode:
            if self.cmds and self.imsis:
                i = int(self.param_map["IMSI_done"][1])
                if i >= len(self.imsis):
                    i = len(self.imsis) - 1
                self.param_map["IMSI_start"][1] = self.imsis[i][0]
                self.param_map["KEY"][1] = self.imsis[i][1]
                self.param_map["OPC"][1] = self.imsis[i][2]
                self.param_map["HPLMN"][1] = self.param_map["HPLMN"][0].text()
                self.param_map["FPLMN"][1] = self.param_map["FPLMN"][0].text()
                self.param_map["SPN"][1] = self.param_map["SPN"][0].text()
            else:
                if not self.cmds and not self.imsis:
                    self.showMessageBox("Load Command file and IMSI file in BatchMode, please")
                else:
                    if not self.cmds:
                        self.showMessageBox("Load Command file in BatchMode, please")
                    else:
                        self.showMessageBox("Load IMSI file in BatchMode, please")
                return -1
        else:
            if self.cmds:
                i = int(self.param_map["IMSI_done"][1])
                self.param_map["IMSI_start"][1] = self.param_map["IMSI_start"][0].text()
                self.param_map["KEY"][1] = self.param_map["KEY"][0].text()
                self.param_map["OPC"][1] = self.param_map["OPC"][0].text()
                self.param_map["HPLMN"][1] = self.param_map["HPLMN"][0].text()
                self.param_map["FPLMN"][1] = self.param_map["FPLMN"][0].text()
                self.param_map["SPN"][1] = self.param_map["SPN"][0].text()
            else:
                self.showMessageBox("Load Command file in SingleMode,please")
                return -1

        self.setIMSI_start()
        self.setKEY()
        self.setOPC()
        self.setHPLMN()
        self.setFPLMN()
        self.setSPN()
        self.textBrowser_Command.setText(self.cmdsToText())
        for k in self.param_map:
            self.param_map[k][0].setText(self.param_map[k][1])
        return 0

    def setHPLMN(self):
        pat_plmn = "XIAOLEZHI-REMARK-PLMN"
        pat_hplmn = "XIAOLEZHI-REMARK-HPLMN"
        pat_oplmn = "XIAOLEZHI-REMARK-OPLMN"
        pat_ehplmn = "XIAOLEZHI-REMARK-EHPLMN"
        for i in range(len(self.cmds)):
            cmd = self.cmds[i]
            if (re.search("//", cmd) and
                    (re.search(pat_plmn, cmd) or
                     re.search(pat_hplmn, cmd) or
                     re.search(pat_oplmn, cmd) or
                     re.search(pat_ehplmn, cmd))):
                plmn = self.param_map["HPLMN"][1]
                if len(plmn) != 5 and len(plmn) != 6:
                    return
                if len(plmn) == 5:
                    plmn = plmn + 'F'
                if len(plmn) != 6:
                    continue
                newcmd = cmd[0:11] + plmn[1] + plmn[0] + plmn[5] + plmn[2] + plmn[4] + plmn[3] + cmd[17:]
                self.cmds[i] = newcmd
        return

    def setFPLMN(self):
        pat = "XIAOLEZHI-REMARK-FPLMN"
        for i in range(len(self.cmds)):
            cmd = self.cmds[i]
            if not re.search("//", cmd) or not re.search(pat, cmd):
                # not matched
                continue
            # matched
            fplmns = self.param_map["FPLMN"][1].split(' ')
            valid = []
            for n in range(len(fplmns)):
                if len(fplmns[n]) == 5 or len(fplmns[n]) == 6:
                    valid.append(fplmns[n])
            fplmns = valid
            tmp = ""
            for n in range(min(len(fplmns), 4)):
                plmn = fplmns[n]
                if (len(plmn) == 5):
                    plmn = plmn + 'F'
                tmp = tmp + plmn[1] + plmn[0] + plmn[5] + plmn[2] + plmn[4] + plmn[3] + ' '
            for n in range(4 - len(fplmns)):
                tmp = tmp + "FFFFFF "
            tmp = tmp[0:27]
            newcmd = cmd[0:11] + tmp + cmd[38:]
            self.cmds[i] = newcmd
        return

    def setIMSI_start(self):
        pat = "XIAOLEZHI-REMARK-IMSI"
        for i in range(len(self.cmds)):
            cmd = self.cmds[i]
            if (not re.search("//", cmd) or not re.search(pat, cmd)):
                #not matched
                continue
            #matched
            imsi = self.param_map["IMSI_start"][1]
            if len(imsi) != 15:
                return
            # add by dongfeng
            pattern = re.compile(imsi_pattern)
            if not pattern.match(imsi):
                self.showMessageBox("imsi invalid!")
                return
            # and end
            newcmd = cmd[0:13]
            newcmd += imsi[0]
            newcmd += cmd[14]
            newcmd += imsi[2]
            newcmd += imsi[1]
            newcmd += imsi[4]
            newcmd += imsi[3]
            newcmd += imsi[6]
            newcmd += imsi[5]
            newcmd += imsi[8]
            newcmd += imsi[7]
            newcmd += imsi[10]
            newcmd += imsi[9]
            newcmd += imsi[12]
            newcmd += imsi[11]
            newcmd += imsi[14]
            newcmd += imsi[13]
            newcmd += cmd[29:]
            self.cmds[i] = newcmd
        return

    def setIMSI_done(self):
        return

    def setKEY(self):
        pat = "XIAOLEZHI-REMARK-KEY"
        for i in range(len(self.cmds)):
            cmd = self.cmds[i]
            if (not re.search("//", cmd) or not re.search(pat, cmd)):
                # not matched
                continue
            # matched
            key = self.param_map["KEY"][1]
            if len(key) != 32:
                return
            newcmd = cmd[0:11] + key.lower() + cmd[43:]
            self.cmds[i] = newcmd
        return

    def setOPC(self):
        pat = "XIAOLEZHI-REMARK-OPC"
        for i in range(len(self.cmds)):
            cmd = self.cmds[i]
            if (not re.search("//", cmd) or not re.search(pat, cmd)):
                # not matched
                continue
            # matched
            opc = self.param_map["OPC"][1]
            if len(opc) != 32:
                return
            newcmd = cmd[0:11] + opc.lower() + cmd[43:]
            self.cmds[i] = newcmd
        return

    def setSPN(self):
        pat = "XIAOLEZHI-REMARK-SPN"
        for i in range(len(self.cmds)):
            cmd = self.cmds[i]
            if (not re.search("//", cmd) or not re.search(pat, cmd)):
                # not matched
                continue
            # matched
            spn = self.param_map["SPN"][1]
            if len(spn) > 16:
                return
            tmp = ""
            for n in range(min(16, len(spn))):
                tmp += "{0}".format(hex(ord(spn[n]))[2:4])
            for n in range(32 - len(tmp)):
                tmp = tmp + 'F'
            newcmd = cmd[0:13] + tmp + cmd[45:]
            self.cmds[i] = newcmd
        return

    def cmdsToText(self):
        text = "<html><body>"
        pat = "XIAOLEZHI-REMARK"
        for cmd in self.cmds:
            tmp1 = "{0}<br>".format(cmd)
            if (re.search(pat, cmd)):
                tmp2 = '<span style=\" color: #0000CD;\">{0}</span>'.format(tmp1)
            else:
                tmp2 = '<span>{0}</span>'.format(tmp1)
            text = "{0}{1}".format(text, tmp2)
        text = "{0}</body></html>".format(text)
        return text

    def imsisToText(self):
        text = "<html><body>"
        for i in range(len(self.imsis)):
            imsi_key_opc = self.imsis[i]
            tmp = "{0} {1} {2}<br>".format(imsi_key_opc[0], imsi_key_opc[1], imsi_key_opc[2])
            if (i == int(self.param_map["IMSI_done"][1])):
                tmp = '<span style=\" color: #ff0000;\">{0}</span>'.format(tmp)
            else:
                tmp = '<span>{0}</span>'.format(tmp)
            text = "{0}{1}".format(text, tmp)
        text = "{0}</body></html>".format(text)
        return text

    def setIMSITextBrowserCursor(self):
        cursor = self.textBrowser_IMSI.textCursor()
        self.textBrowser_IMSI.moveCursor(cursor.Start)
        max = int(self.param_map["IMSI_done"][1])
        for i in range(0, max):
            self.textBrowser_IMSI.moveCursor(cursor.Down)

    def loadCommandFile(self):
        file_name, ok = QFileDialog.getOpenFileName(self, "Open a file to import commands", "", "", "")
        if ok:
            self.cmds.clear()
            file_handle = open(file_name, 'r')
            items = file_handle.readlines()
            file_handle.close()
            for item in items:
                cmd = re.split("\n|\r", item)
                if cmd[0] == "":
                    continue
                self.cmds.append(cmd[0])
            self.textBrowser_Command.setText(self.cmdsToText())
            self.statusBar.showMessage("succeed read from " + file_name + " for commands")
            self.setParamMap()
        else:
            self.statusBar.showMessage("failed to read from " + file_name + " for commands")
        return


    def loadIMSIFile(self):
        file_name, ok = QFileDialog.getOpenFileName(self, "Open a file to import IMSIs", "", "", "")
        if ok:
            self.imsis.clear()
            file_handle = open(file_name, 'r')
            items = file_handle.readlines()
            file_handle.close()
            for item in items:
                imsi_key_opc = re.split(" |\t|\n|\r", item)[0:3]
                if (len(imsi_key_opc) == 0 or imsi_key_opc[0] == ""):
                    continue
                # add by dongfeng
                pattern = re.compile(imsi_pattern)
                if not pattern.match(imsi_key_opc[0]):
                    self.showMessageBox("one or more imsi(s) invalid! Please check and reload!")
                    self.reset()
                    return -1					
                # add end
                self.imsis.append(imsi_key_opc)
            self.textBrowser_IMSI.setText(self.imsisToText())
            self.setIMSITextBrowserCursor()
            self.statusBar.showMessage("succeed read from " + file_name + " for imsis")
            self.setParamMap()
        else:
            self.statusBar.showMessage("failed to read from " + file_name + " for imsis")
        return

    def doSingleIMSI(self):
        self.menuChooseMode.setTitle("SingleMode")
        self.batch_mode = False
        self.reset()
        if (self.cmds != []):
            self.setParamMap()
        return

    def doBatchIMSI(self):
        self.menuChooseMode.setTitle("BatchMode")
        self.batch_mode = True
        self.reset()
        if (self.cmds != []):
            self.setParamMap()
        return

    def initCard(self):
        try:
            rs = readers()
            for r in rs:
                connection = r.createConnection()
                break
            if 'connection' in dir():
                self.cardconn = connection
                return 0
            else:
                self.showMessageBox("Writer is not connected!")
                return -1
        except:
            self.showMessageBox("No card is in writer!")
            return -1

    def showMessageBox(self, msg, icon = QMessageBox.Critical):
        box = QMessageBox()
        box.setIcon(icon)
        box.setText(msg)
        box.setWindowTitle("MessageBox")
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()

    def readCard(self):
        self.cardconn.connect()
        #read imsi
        imsi_cmds = [
            "00A4000C02 3F00",
            "00A4000C02 7F20",
            "00A4000C02 6F07",
            "00B0000009 "
        ]
        for cmd in imsi_cmds:
            instruction = cmd.replace(" ", "")
            print("instruction={0} {1}".format(instruction[0:10], instruction[10:]))
            response, sw1, sw2 = self.cardconn.transmit(toBytes(instruction))
            s = toHexString(response).replace(" ", "")
            print("response=[{0}], sw1=[{1}], sw2=[{2}]".format(s, hex(sw1), hex(sw2)))
            if (sw1 != 0x90 or sw2 != 0x0):
                self.showMessageBox("Read imsi error!")
                exit(-1)
        if (len(s) != 18):
            self.showMessageBox("Read imsi len error!")
            exit(-1)
        imsi = s[2] + s[5] + s[4] + s[7] + s[6] + s[9] + s[8] + s[11] + s[10] + s[13] + s[12] + s[15] + s[14] + s[17] + s[16]
        # add by dongfeng
        pattern = re.compile(imsi_pattern)
        if not pattern.match(imsi):
            self.showMessageBox("imsi invalid!")
            return
        # add end

        # read hplmn
        hplmn_cmds = [
            "00A4000C02 3F00",
            "00A4000C02 7FF0",
            "00A4000C02 6F60",
            "00B0000041 "
        ]
        for cmd in hplmn_cmds:
            instruction = cmd.replace(" ", "")
            print("instruction={0} {1}".format(instruction[0:10], instruction[10:]))
            response, sw1, sw2 = self.cardconn.transmit(toBytes(instruction))
            s = toHexString(response).replace(" ", "")
            print("response=[{0}], sw1=[{1}], sw2=[{2}]".format(s, hex(sw1), hex(sw2)))
            if (sw1 != 0x90 or sw2 != 0x0):
                self.showMessageBox("Read hplmn error!")
                exit(-1)
        if (len(s) != 130):
            self.showMessageBox("Read hplmn len error!")
            exit(-1)
        if (s[2] != 'F'):
            hplmn = s[1] + s[0] + s[3] + s[5] + s[4] + s[2]
        else:
            hplmn = s[1] + s[0] + s[3] + s[5] + s[4]
        # read fplmn
        fplmn_cmds = [
            "00A4000C02 3F00",
            "00A4000C02 7FF0",
            "00A4000C02 6F7B",
            "00B000000C "
        ]
        for cmd in fplmn_cmds:
            instruction = cmd.replace(" ", "")
            print("instruction={0} {1}".format(instruction[0:10], instruction[10:]))
            response, sw1, sw2 = self.cardconn.transmit(toBytes(instruction))
            s = toHexString(response).replace(" ", "")
            print("response=[{0}], sw1=[{1}], sw2=[{2}]".format(s, hex(sw1), hex(sw2)))
            if (sw1 != 0x90 or sw2 != 0x0):
                self.showMessageBox("Read fplmn error!")
                exit(-1)
        if (len(s) != 24):
            self.showMessageBox("Read fplmn len error!")
            exit(-1)
        fplmns = ""
        for i in range(int(len(s)/6)):
            n = i*6
            if s[2+n] != 0xF:
                fplmn = "{0}{1}{2}{3}{4}{5}".format(s[1+n], s[0+n], s[3+n], s[5+n], s[4+n], s[2+n])
            else:
                fplmn = "{0}{1}{2}{3}{4}".format(s[1+n], s[0+n], s[3+n], s[5+n], s[4+n])
            print("{0},{1}".format(i, fplmn))
            if (fplmn == "FFFFFF"):
                break
            if len(fplmn) == 6 and fplmn[5] == 'F':
                fplmn = fplmn[0:5]
            if (fplmns == ""):
                fplmns = fplmn
            else:
                fplmns = fplmns + " " + fplmn

        # read spn
        spn_cmds = [
            "00A4000C02 3F00",
            "00A4000C02 7FF0",
            "00A4000C02 6F46",
            "00B0000011 "
        ]
        for cmd in spn_cmds:
            instruction = cmd.replace(" ", "")
            print("instruction={0} {1}".format(instruction[0:10], instruction[10:]))
            response, sw1, sw2 = self.cardconn.transmit(toBytes(instruction))
            s = toHexString(response).replace(" ", "")
            print("response=[{0}], sw1=[{1}], sw2=[{2}]".format(s, hex(sw1), hex(sw2)))
            if (sw1 != 0x90 or sw2 != 0x0):
                self.showMessageBox("Read spn error!")
                exit(-1)
        if (len(s) != 34):
            self.showMessageBox("Read spn len error!")
            exit(-1)
        for i in range(int(len(s) / 2)):
            n = i * 2
            if (s[n] == 'F' and s[n+1] == 'F'):
                i = i - 1
                break
        resp = response[1:i+1]
        spn = ""
        for i in range(len(resp)):
            spn = spn + chr(resp[i])

        msg = "IMSI:{0}\n" \
              "HPLMN:{1}\n" \
              "FPLMNs:{2}\n" \
              "SPN:{3}".format(imsi, hplmn, fplmns, spn)
        self.showMessageBox(msg, QMessageBox.Information)
        self.statusBar.showMessage("Read card success!")
        return

    def writeCard(self):
        self.cardconn.connect()
        if not self.cmds:
            return
        if not self.batch_mode or (self.batch_mode and int(self.param_map["IMSI_done"][1]) < len(self.imsis)):
            self.setParamMap()
        for cmd in self.cmds:
            subs = re.split("//", cmd.strip("\n\r"))
            if len(subs) == 0:
                continue
            if subs[0] == '':
                continue
            instruction = subs[0].replace(' ', '')
            if instruction == '':
                continue
            if instruction[0] == ';':
                continue
            if len(instruction) < 10:
                continue
            print("instruction={0} {1}".format(instruction[0:10], instruction[10:]))
            response, sw1, sw2 = self.cardconn.transmit(toBytes(instruction))
            print("response=[{0}], sw1=[{1}], sw2=[{2}]".format(toHexString(response), hex(sw1), hex(sw2)))
            if (sw1 != 0x90) and (sw1 != 0x61):
                self.showMessageBox("Write usim error!")
                exit(-1)

        if not self.batch_mode:
            self.param_map["IMSI_done"][1] = "{0}".format(int(self.param_map["IMSI_done"][1]) + 1)
            self.param_map["IMSI_done"][0].setText(self.param_map["IMSI_done"][1])
            self.setParamMap()
        else:
            if int(self.param_map["IMSI_done"][1]) < len(self.imsis):
                self.param_map["IMSI_done"][1] = "{0}".format(int(self.param_map["IMSI_done"][1])+1)
            self.param_map["IMSI_done"][0].setText(self.param_map["IMSI_done"][1])
            if int(self.param_map["IMSI_done"][1]) < len(self.imsis):
                self.setParamMap()
            self.textBrowser_IMSI.setText(self.imsisToText())
            self.setIMSITextBrowserCursor()
            if int(self.param_map["IMSI_done"][1]) >= len(self.imsis):
                self.showMessageBox("All IMSIs done")

        self.statusBar.showMessage("Write card success!")
        return


    def doAbout(self):
        buttonReply = QMessageBox.about(self, 'About', "USIM Writer version ks2.0(2019-10-10) for internal only\n"
                                                       "Any question, please email to lezixiao@qq.com")

    def doExit(self):
        sys.exit(0)

class MyBrower():
    def __init__(self, log):
        self.log = log

    def write(self, s):
        self.log.append(s)

    def flush(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    rv = myshow.initCard()
    if rv != 0:
        sys.exit(rv)
    sys.exit(app.exec_())
