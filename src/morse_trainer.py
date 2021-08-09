import socket
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,  \
            QVBoxLayout,QHBoxLayout,QLineEdit,QTextEdit,QLabel,QCheckBox, \
            QPushButton,QRadioButton,QComboBox    


class App(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'Morse Trainer'
        self.initUI()

    def initUI(self):
        connbtn = QPushButton("CONNECT",self)
        iplbl = QLabel("Host IP:")
        portlbl = QLabel("Port:")
        self.ipadr = QLineEdit()
        self.port = QLineEdit()
        self.ipadr.setText("192.168.1.5")
        self.port.setText("8888")
        voidlbl = QLabel("")
        voidlbl.setMinimumWidth(5)
        speedbtn = QPushButton("SET",self)
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
        hhome.addWidget(connbtn)
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
        hbot = QHBoxLayout()
        hbot.addWidget(self.xmt)
        hbot.addWidget(self.rcv)
        self.layout = QVBoxLayout(self)
        self.layout.addLayout(hhome) 
        self.layout.addLayout(hmed)
        self.layout.addLayout(hbot)
        sendbtn = QPushButton("SEND DATA",self)
        self.layout.addWidget(sendbtn)
        #hhome.addWidget(voidlbl)
        self.setGeometry(100, 50, 620,400)
        self.show()


def invia_comandi(s):
    while True:
        comando = input("-> ")
        if comando == "ESC":
            print("Sto chiudendo la connessione col Server.")
            s.close()
            sys.exit()
        else:
            comando = comando+"\r\n"
            s.send(comando.encode())
            data = s.recv(4096)
            print(str(data, "utf-8"))

def conn_sub_server(indirizzo_server):
    try:
        s = socket.socket()             # creazione socket client
        s.connect(indirizzo_server)     # connessione al server
        print(f"Connessessione al Server: { indirizzo_server } effettuata.")
    except socket.error as errore:
        print(f"Qualcosa è andato storto, sto uscendo... \n{errore}")
        sys.exit()
    data = s.recv(4096)
    print(str(data, "utf-8"))
    invia_comandi(s)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())  
    #conn_sub_server(("192.168.1.5", 8888))