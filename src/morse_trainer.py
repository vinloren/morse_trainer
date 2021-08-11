import socket
import sys
import random
import threading
import datetime
import time
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
        self.radiob = QRadioButton("Send 10 groups of 5 random chars")
        self.radiob1 = QRadioButton("Automatic sending groups of 5 chars")
        self.radiob2 = QRadioButton("Send from transmit box")
        self.radiob.clicked.connect(self.checkb)
        self.radiob1.clicked.connect(self.checkb1)
        self.radiob2.clicked.connect(self.checkb2)
        hlast = QHBoxLayout()
        hlast.addWidget(self.radiob)
        hlast.addWidget(self.radiob1)
        hlast.addWidget(self.radiob2)
        self.layout.addLayout(hlast)
        self.sendbtn = QPushButton("SEND DATA",self)
        self.sendbtn.clicked.connect(self.send_click)
        self.layout.addWidget(self.sendbtn)
        self.radiob2.setChecked(True)
        #hhome.addWidget(voidlbl)
        self.setGeometry(100, 50, 620,400)
        self.show()

    def checkb(self):
        print("Invio 10 gruppi di 5 chars")
        self.sendbtn.setEnabled(True)

    def checkb1(self):
        print("Invio continuo di 10 gruppi di 5 chars")
        self.sendbtn.setEnabled(False)

    def checkb2(self):
        print("Invio da transmit box")
        self.sendbtn.setEnabled(True)


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
            self.rt.stop()
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
            self.inviaGruppi()
        data = self.s.recv(4096)
        self.rcv.append(str(data,"utf-8"))
        print(str(data, "utf-8"))


    def set_speed_click(self):
        speed = self.cmbspeed.currentText()
        print(speed)
        self.invia_comandi(speed)
        data = self.s.recv(4096)
        print(str(data, "utf-8"))
        self.rcv.append(speed+' '+str(data,"utf-8"))


    def tone_click(self):
        tone = self.cmbtone.currentText()
        print("Tone Hz: "+tone )
        self.invia_comandi(tone)
        data = self.s.recv(4096)
        print(str(data, "utf-8"))
        self.rcv.append("Tone "+tone+'Hz '+str(data,"utf-8"))


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
        self.rt = RepeatedTimer(120, ex.sendText) # no need of rt.start()


    def sendText(self): # called every x seconds
        currTime = datetime.datetime.now().strftime("%H:%M:%S")
        if(self.radiob1.isChecked() == False):
            print("Nothing to do at "+currTime)
        else:
            self.rcv.append("Inizio trasmissione 10 gruppi 5chars at "+currTime)
            self.inviaGruppi()
            

    def inviaGruppi(self):
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
        self.invia_comandi(s)
        data = self.s.recv(4096)
        self.rcv.append(str(data,"utf-8"))
        print(str(data, "utf-8"))
        self.xmt.append(s)


    def invia_comandi(self,comando):
        if comando == "ESC":
            print("Sto chiudendo la connessione col Server.")
            self.s.close()
            sys.exit()
        else:
            comando = comando+"\r\n"
            self.s.send(comando.encode())
            
            

class RepeatedTimer(object): # Timer helper class
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True
      print("Timer app started")

  def stop(self):
    self._timer.cancel()
    self.is_running = False



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())  