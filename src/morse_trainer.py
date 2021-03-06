from os import defpath, truncate
import socket
import sys
import random
import threading
import datetime
import time
from typing import Text
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,  \
            QVBoxLayout,QHBoxLayout,QLineEdit,QTextEdit,QLabel,QCheckBox, \
            QPushButton,QRadioButton,QComboBox,QLineEdit   

TIME_LIMIT = 120
clientSock = socket.socket()
recvData = ""
sendData = ""
host = "192.168.1.5"
port = 8888
CONNECTED = False
INVIA = False
RICEVI = False
GRUPPI = False

class App(QWidget):
    
    CONNECTED = False
    charspace = 1
    datachrs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', \
                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',\
                'w', 'x', 'y', 'z','1','2','3','4','5','6','7','8','9','0', \
                '?','/',',','.','=']
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Morse Trainer')
        self.setFixedSize(630, 400)
        self.initUI()

    def initUI(self):
        self.connbtn = QPushButton("CONNECT",self)
        self.connbtn.setCheckable(True)
        self.connbtn.clicked.connect(self.connect_click)
        iplbl = QLabel("Host IP:")
        portlbl = QLabel("Port:")
        self.ipadr = QLineEdit()
        self.port = QLineEdit()
        self.ipadr.setText("192.168.1.5")
        self.port.setText("8888")
        #voidlbl = QLabel("")
        #voidlbl.setMinimumWidth(30)
        speedbtn = QPushButton("SET",self)
        speedbtn.clicked.connect(self.set_speed_click)
        speedbtn.setMaximumWidth(50)
        lblspeed = QLabel("Speed:")
        self.cmbspeed = QComboBox(self)
        self.cmbspeed.addItem('5wpm')
        self.cmbspeed.addItem('10wpm')
        self.cmbspeed.addItem('15wpm')
        self.cmbspeed.addItem('20wpm')
        self.cmbspeed.addItem('25wpm')
        self.cmbspeed.addItem('30wpm')
        tonebtn = QPushButton("SET",self)
        tonebtn.clicked.connect(self.tone_click)
        tonebtn.setMaximumWidth(50)
        lbltone = QLabel("Tone Hz:")
        self.cmbtone = QComboBox(self)
        self.cmbtone.addItem('400')
        self.cmbtone.addItem('500')
        self.cmbtone.addItem('600')
        self.cmbtone.addItem('700')
        self.cmbtone.addItem('800')
        self.cmbtone.addItem('900')
        hhome = QHBoxLayout()
        hhome.addWidget(self.connbtn)
        hhome.addWidget(iplbl)
        self.ipadr.setMaximumWidth(80)
        hhome.addWidget(self.ipadr)
        hhome.addWidget(portlbl)
        self.port.setMaximumWidth(45)
        hhome.addWidget(self.port)
        hhome.addWidget(speedbtn)
        hhome.addWidget(lblspeed)
        hhome.addWidget(self.cmbspeed)
        hhome.addWidget(tonebtn)
        hhome.addWidget(lbltone)
        hhome.addWidget(self.cmbtone)
        hmed = QHBoxLayout()
        xmtlbl = QLabel("Transmit")
        self.vblbl = QLabel("Vbatt: n/a")
        self.vblbl.setMinimumWidth(144)
        xmtlbl.setMinimumWidth(153)
        rcvlbl = QLabel("Receive")
        self.spbchr = QCheckBox("Double space between chars")
        self.spbchr.clicked.connect(self.spbchr_click)
        self.xmt = QTextEdit()
        self.xmt.setFontFamily("courier")
        self.rcv = QTextEdit()
        self.rcv.setFontFamily("courier")
        hmed.addWidget(xmtlbl)
        hmed.addWidget(self.vblbl)
        hmed.addWidget(rcvlbl)
        hmed.addWidget(self.spbchr)
        hnbot = QHBoxLayout()
        clearsnd = QPushButton("CLEAR",self)
        clearrcv = QPushButton("CLEAR",self)
        clearsnd.clicked.connect(self.clear_snd)
        clearrcv.clicked.connect(self.clear_rcv)
        hnbot.addWidget(clearsnd)
        hnbot.addWidget(clearrcv)
        hbot = QHBoxLayout()
        hbot.addWidget(self.xmt)
        hbot.addWidget(self.rcv)
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(hhome) 
        self.layout.addLayout(hmed)
        self.layout.addLayout(hbot)
        self.layout.addLayout(hnbot)
        self.radiob = QRadioButton("Send 10 groups of 5 random chars")
        self.radiob1 = QRadioButton("Automatic sending groups of chars")
        self.radiob2 = QRadioButton("Send from transmit box")
        self.repeat = QCheckBox("Repeat send")
        self.radiob.clicked.connect(self.checkb)
        self.radiob1.clicked.connect(self.checkb1)
        self.radiob2.clicked.connect(self.checkb2)
        hlast = QHBoxLayout()
        hlast.addWidget(self.radiob)
        hlast.addWidget(self.radiob1)
        hlast.addWidget(self.radiob2)
        hlast.addWidget(self.repeat)
        self.layout.addLayout(hlast)
        hnlast = QHBoxLayout()
        self.ckbutt =  QPushButton("CHECK TEST",self)
        self.intext = QLineEdit()
        hnlast.addWidget(self.ckbutt)
        hnlast.addWidget(self.intext)
        self.ckbutt.clicked.connect(self.checktest)
        self.ckbutt.setEnabled(False)
        self.layout.addLayout(hnlast)
        self.sendbtn = QPushButton("SEND DATA",self)
        self.sendbtn.clicked.connect(self.send_click)
        self.layout.addWidget(self.sendbtn)
        self.radiob2.setChecked(True)
        self.setGeometry(100, 50, 630,400)
        self.show()


    def spbchr_click(self):
        if(self.spbchr.isChecked() == True):
            print("Double space")
            self.charspace = 2
        else:
            print("Single space")
            self.charspace = 1

    def checkb(self):
        self.sendbtn.setEnabled(True)

    def checkb1(self):
        currTime = datetime.datetime.now().strftime("%H:%M:%S")
        self.rcv.append("Invio continuo di 10 gruppi di 5 chars at: "+currTime)
        self.repeatSend.start()
        self.sendbtn.setEnabled(False)

    def checkb2(self):
        print("Invio da transmit box")
        self.sendbtn.setEnabled(True)

    def checktest(self):
        print("checktest")
        text = self.intext.text()
        text = text.upper()
        global sendData
        # compara dati scritti in intext capiti da morse code con
        # quelli realmente trasmessi. Riporta errori in rcv box.
        words = sendData.strip().split(' ')
        print(str(len(words))+" gruppi")
        if(len(words) != 10):
            self.rcv.append("Non ci sono gruppi da verificare.")
            return
        else:
            for word in words:
                if(len(word) != 5):
                    self.rcv.append("Non ci sono gruppi da verificare.")
                    return    
        ok = 0
        if(text == ""):
            self.rcv.append("CHECK TEST ?? vuoto.")
            return
        test = text.split(' ')
        i = 0
        for testo in test:
            if (len(testo) == 5):
                i += 1
        if(i != 10):
            self.rcv.append("CHECK TEST non contiene 10 gruppi di 5 chars.")
            return
        indice = []
        errs = 0
        terrs = 0
        i = 0
        while(i < len(words)):
            if(words[i] == test[i]):
                ok += 1
            else:
                indice.append(i)
            i += 1
            
        if(ok == len(words)):
            self.rcv.append("Tutti i gruppi ricevuti sono corretti.")
        else:
            for i in indice:
                reale = words[i]
                rcvt = test[i]
                j = 0
                while(j<5):
                    if(reale[j] != rcvt[j]):
                        errs += 1
                    j += 1
                msg = "Reale "+reale+" Ricevuto "+rcvt+" "+str(errs)+" err"
                print(msg)
                self.rcv.append(msg)
                terrs += errs
                errs = 0
            msg = "Totale errori: "+str(terrs)+" su 50 chars."
            print(msg)
            self.rcv.append(msg)


    def clear_snd(self):
        self.xmt.clear()

    def clear_rcv(self):
        self.rcv.clear()

    def connect_click(self):
        if self.connbtn.isChecked():
            self.connbtn.setText("CLOSE")
        else:
            self.connbtn.setText("CONNECT")

        if(self.connbtn.text( ) == "CLOSE"):
            global host
            global port
            global clientSock 
            clientSock.close()
            clientSock = socket.socket()
            host = self.ipadr.text()
            port = int(self.port.text())
            self.tcpClient = clientTCP()
            self.tcpClient.actionDone.connect(self.onTCPflag)
            self.conn_sub_server()
        else:
            self.invia_comandi("ESC") 


    def conn_sub_server(self):
        try:
            global host
            global port
            clientSock.connect((host,port))     # connessione al server
            print(f"Connessessione al Server: { (host,port) } effettuata.")
            self.CONNECTED = True
            self.repeatSend = RepeatedTimer()
            self.repeatSend.countChanged.connect(self.onCountChanged)
            self.tcpClient.start()
            self.ckbutt.setEnabled(True)
        except socket.error as errore:
            print(f"Azz.. qualcosa ?? andato storto, sto uscendo... \n{errore}")
            sys.exit()


    def invia_comandi(self,comando):
        global sendData
        sendData = comando
        if comando == "ESC":
            print("Sto chiudendo la connessione col Server.")
            clientSock.close()
            self.rcv.append("Chiuso connessione con host")
            self.CONNECTED = False
        else:
            comando = comando+"\r\n"
            clientSock.send(comando.encode())
            

    def inviaGruppi(self):
        global GRUPPI
        GRUPPI = True
        i = 0
        j = 0
        s = ""
        while(i<10):
            while(j<5):
                x = random.randint(0,len(self.datachrs)-1)
                s += self.datachrs[x]
                j += 1
            s += ' '
            i += 1
            j = 0
        s = s.upper()
        print(s)
        currTime = datetime.datetime.now().strftime("%H:%M:%S")
        self.invia_comandi(s)


    def send_click(self):
        if(self.CONNECTED == True):
            if(self.radiob.isChecked() == False):
                data = self.xmt.toPlainText()
                riga = data.split("\n")
                l = len(riga)
                testo = riga[l-2]
                print(testo) # stampa ultima riga (da ultimo \n in poi)
                self.invia_comandi(testo)
            else:
                # crea 10 gruppi random di 5 chars in una stringa
                currTime = datetime.datetime.now().strftime("%H:%M:%S")
                self.rcv.append("Inizio trasmissione 10 gruppi 5chars at: "+currTime)
                self.inviaGruppi()
        

    def set_speed_click(self):
        speed = self.cmbspeed.currentText()
        if(self.CONNECTED == True):
            print(speed)
            self.invia_comandi(speed)
           
    def tone_click(self):
        tone = self.cmbtone.currentText()
        if(self.CONNECTED == True):
            print("Tone Hz: "+tone )
            self.invia_comandi(tone)

    def onTCPflag(self,value):
        global rcvData
        global sendData
        global GRUPPI
        global TIME_LIMIT
        if(value == 2): # ricevuto dati
            print(rcvData)
            if(GRUPPI == True):
                GRUPPI = False
                self.xmt.append(sendData)
                currTime = datetime.datetime.now().strftime("%H:%M:%S")
                self.rcv.append("Fine tramissione gruppi at: "+currTime)
            elif(sendData[2:5] == "wpm" or sendData[1:4] == "wpm"):
                self.rcv.append(sendData+" "+rcvData)
                if(sendData == "5wpm"):
                    TIME_LIMIT = 210
                else:
                    TIME_LIMIT = 120
                sp = "charspace"+str(self.charspace)
                self.invia_comandi(sp)
            elif(sendData == "charspace2"):
                TIME_LIMIT = 2*TIME_LIMIT
                self.rcv.append(sendData+" "+rcvData)
            elif(sendData == "charspace1"):
                self.rcv.append(sendData+" "+rcvData)
            elif(sendData[1:3] == "00"):
                self.rcv.append("Tone "+sendData+"Hz "+rcvData)
            else: 
                if(sendData == "" or sendData == "ESC"):
                    self.rcv.append(rcvData)
                else:
                    self.rcv.append(sendData+" "+rcvData)
                    if(self.repeat.isChecked() == True):
                        if(self.radiob1.isChecked() == False):
                            time.sleep(2)
                            self.invia_comandi(sendData)
        elif(value == 3): # ricevuto vbatt
            vbatt = "Vbatt: "+rcvData
            self.vblbl.setText(vbatt)


    def onCountChanged(self, value):
        currTime = datetime.datetime.now().strftime("%H:%M:%S")
        if(self.radiob1.isChecked() == False):
            print("Nothing to do at "+currTime)
        else:
            if(value == 0):
                self.rcv.append("Inizio trasmissione 10 gruppi 5chars at "+currTime)
                self.inviaGruppi()
            else:
                self.repeatSend.start()


    
class clientTCP(QThread):
    actionDone = pyqtSignal(int)
    RUNNING = True
    
    def run(self):
        print("clientTCP started")
        while(self.RUNNING == True):  
            global rcvData
            try:
                rcvData = clientSock.recv(4096)
                rcvData = str(rcvData,"utf-8")
                if(rcvData == "Ack"):
                    self.actionDone.emit(2)
                elif(rcvData[0:2] == "3."):
                    self.actionDone.emit(3)
                else:
                    self.actionDone.emit(2)    
            except:
                self.RUNNING = False
        print("clientTCP terminated")
   

class RepeatedTimer(QThread):
    countChanged = pyqtSignal(int)
    def run(self):
        print("Start timer")
        count = 0
        self.countChanged.emit(count)
        while count < TIME_LIMIT:
            count +=1
            time.sleep(1)
        print("Raggiunto limite tempo")
        self.countChanged.emit(count)

    def stop(self):
        self.is_running = False
        self.terminate()
         


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())  