import socket
import sys
import random
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,  \
            QVBoxLayout,QHBoxLayout,QLineEdit,QTextEdit,QLabel,QCheckBox, \
            QPushButton,QRadioButton,QComboBox    


class App(QWidget):
    s = socket.socket()
    CONNECTED = False
    datachrs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', \
                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',\
                 'w', 'x', 'y', 'z','1','2','3','4','5','6','7','8','9','0', \
                 '?','/',',','.','=']

    def __init__(self):
        super().__init__()
        self.title = 'Morse Trainer'
        self.initUI()

    def initUI(self):
        self.connbtn = QPushButton("CONNECT",self)
        self.connbtn.clicked.connect(self.connect_click)
        iplbl = QLabel("Host IP:")
        portlbl = QLabel("Port:")
        self.ipadr = QLineEdit()
        self.port = QLineEdit()
        self.ipadr.setText("192.168.1.5")
        self.port.setText("8888")
        voidlbl = QLabel("")
        voidlbl.setMinimumWidth(5)
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
        rcvlbl = QLabel("Receive")
        self.xmt = QTextEdit()
        self.rcv = QTextEdit()
        hmed.addWidget(xmtlbl)
        hmed.addWidget(rcvlbl)
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
        self.radiob = QRadioButton("send 10 groups of 5 random chars each in place of data in transmit box")
        self.layout.addWidget(self.radiob)
        sendbtn = QPushButton("SEND DATA",self)
        sendbtn.clicked.connect(self.send_click)
        self.layout.addWidget(sendbtn)
        #hhome.addWidget(voidlbl)
        self.setGeometry(100, 50, 620,400)
        self.show()

    def clear_snd(self):
        self.xmt.clear()

    def clear_rcv(self):
        self.rcv.clear()

    def connect_click(self):
        if(self.CONNECTED == False):
            host = self.ipadr.text()
            port = int(self.port.text())
            self.conn_sub_server((host,port))  
        else:
            self.invia_comandi("ESC") 

    def send_click(self):
        if(self.radiob.isChecked() == False):
            data = self.xmt.toPlainText()
            riga = data.split("\n")
            l = len(riga)
            testo = riga[l-2]
            print(testo) # stampa ultima riga (da ultimo \n in poi)
            self.invia_comandi(testo)
        else:
            # crea 10 gruppi random di 5 chars in una stringa
            print("preparo 10 gruppi di 5 chars")
            i = 0
            j = 0
            pacchetto = []
            while(i<10):
                while(j<5):
                    x = random.randint(0,len(self.datachrs)-1)
                    pacchetto.append(self.datachrs[x])
                    j += 1
                pacchetto.append(' ')
                #print(str(pacchetto))
                i += 1
                j = 0
            #print(pacchetto)
            s = ""
            for x in pacchetto:
                s += x 
            print(s)
            self.invia_comandi(s)
            self.xmt.append(s)

    def set_speed_click(self):
        speed = self.cmbspeed.currentText()
        print(speed)
        self.invia_comandi(speed)


    def tone_click(self):
        tone = self.cmbtone.currentText()
        print("Tone Hz: "+tone )
        self.invia_comandi(tone)


    def conn_sub_server(self,indirizzo_server):
        try:
            #s = socket.socket()             # creazione socket client
            self.s.connect(indirizzo_server)     # connessione al server
            print(f"Connessessione al Server: { indirizzo_server } effettuata.")
            self.CONNECTED = True
            self.connbtn.setText("CLOSE")
        except socket.error as errore:
            print(f"Qualcosa è andato storto, sto uscendo... \n{errore}")
            sys.exit()
        data = self.s.recv(4096)
        print(str(data, "utf-8"))
        self.rcv.append(str(data,"utf-8"))


    def invia_comandi(self,comando):
        if comando == "ESC":
            print("Sto chiudendo la connessione col Server.")
            self.s.close()
            sys.exit()
        else:
            comando = comando+"\r\n"
            self.s.send(comando.encode())
            data = self.s.recv(4096)
            self.rcv.append(str(data,"utf-8"))
            print(str(data, "utf-8"))
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())  