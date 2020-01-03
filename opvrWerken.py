from login import hoofdMenu
import datetime
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QGridLayout, QTableView,\
          QComboBox, QDialog, QLineEdit, QMessageBox, QVBoxLayout
from sqlalchemy import (Table, Column, Integer, String, MetaData,\
                        create_engine, Float)
from sqlalchemy.sql import select, update

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Externe werken opvragen')               
    msg.exec_() 

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Externe werken opvragen')               
    msg.exec_() 

def jaarweek():
    dt = datetime.datetime.now()
    week = str(dt.isocalendar()[1])
    jaar = str(dt.isocalendar()[0])
    if len(week)== 1:
        week = '0'+week
    jrwk = jaar+week
    return(jrwk)
    
def werkenKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Financieël Overzicht Werken")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Times', 10))
    
            self.Keuze4 = QLabel()
            k4Edit = QComboBox()
            k4Edit.setFixedWidth(330)
            k4Edit.setFont(QFont("Times", 10))
            k4Edit.setStyleSheet("color: black;  background-color: gainsboro")
            k4Edit.addItem('              Sorteersleutel voor zoeken')
            k4Edit.addItem('1. Alle werken')
            k4Edit.addItem('2. Werknummer')
            k4Edit.addItem('3. Werkomschrijving')
            k4Edit.addItem('4. Voortgangstatus.')
            k4Edit.addItem('5. Aanneemsom >')
            k4Edit.addItem('6. Aanneemsom <')
            k4Edit.addItem('7. Afgerekend in % >')
            k4Edit.activated[str].connect(self.k4Changed)
            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(210)
            zktermEdit.setFont(QFont("Times", 10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                                  
            grid.addWidget(k4Edit, 1, 0, 1, 2, Qt.AlignRight)
            lbl1 = QLabel('Zoekterm')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 2, 0)
            grid.addWidget(zktermEdit, 2, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 6, 0, 1, 2, Qt.AlignRight)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
    
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
            
            sluitBtn = QPushButton('Sluiten')
            sluitBtn.clicked.connect(lambda: windowSluit(self, m_email))
            
            grid.addWidget(applyBtn, 5, 1, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial", 10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(sluitBtn, 5, 1)
            sluitBtn.setFont(QFont("Arial", 10))
            sluitBtn.setFixedWidth(100)
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro")
       
        def k4Changed(self, text):
            self.Keuze4.setText(text)
            
        def zktermChanged(self, text):
            self.Zoekterm.setText(text)
 
        def returnk4(self):
            return self.Keuze4.text()
        
        def returnzkterm(self):
            return self.Zoekterm.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk4(), dialog.returnzkterm()]       

    window = Widget()
    data = window.getData()
    if not data[0] or data[0][0] == ' ':
        keuze = 0
    elif data[0]:
        keuze = int(data[0][0])
    else:
        keuze = 0
    if data[1]:
        zoekterm = data[1]
    else:
        zoekterm = ''
    toonWerken(keuze,zoekterm, m_email)
 
def toonWerken(keuze,zoekterm, m_email): 
    import validZt      
    metadata = MetaData()
    werken = Table('werken', metadata,
        Column('werknummerID', Integer(), primary_key=True),
        Column('werkomschrijving', String),
        Column('voortgangstatus', String),
        Column('statusweek',  String),
        Column('startweek', String),
        Column('opdracht_datum', String),
        Column('aanneemsom', Float),
        Column('betaald_bedrag', Float),
        Column('begr_materialen', Float),
        Column('kosten_materialen', Float),
        Column('begr_lonen', Float),
        Column('kosten_lonen', Float),
        Column('begr_materieel',Float),
        Column('kosten_materieel', Float), 
        Column('begr_leiding', Float),
        Column('kosten_leiding', Float),
        Column('begr_huisv', Float),
        Column('kosten_huisv', Float),
        Column('begr_inhuur', Float),
        Column('kosten_inhuur', Float),
        Column('begr_overig', Float),
        Column('kosten_overig', Float),
        Column('begr_vervoer', Float),
        Column('kosten_vervoer', Float),
        Column('begr_beton_bvl', Float),
        Column('beton_bvl', Float),
        Column('begr_kabelwerk', Float),
        Column('kabelwerk', Float),
        Column('begr_grondverzet', Float),
        Column('grondverzet', Float),
        Column('meerminderwerk', Float),
        Column('begr_constr_uren', Float),
        Column('werk_constr_uren', Float),
        Column('begr_mont_uren', Float),
        Column('werk_mont_uren', Float),
        Column('begr_retourlas_uren', Float),
        Column('werk_retourlas_uren', Float),
        Column('begr_telecom_uren', Float),
        Column('werk_telecom_uren', Float),
        Column('begr_bfi_uren', Float),
        Column('werk_bfi_uren', Float),
        Column('begr_bvl_uren', Float),
        Column('werk_bvl_uren', Float),
        Column('begr_voeding_uren', Float),
        Column('werk_voeding_uren', Float),
        Column('begr_spoorleg_uren',  Float),
        Column('werk_spoorleg_uren', Float),
        Column('begr_spoorlas_uren', Float),
        Column('werk_spoorlas_uren', Float),
        Column('begr_reis_uren', Float),
        Column('werk_reis_uren', Float))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
  
    if keuze == 1:
        sel = select([werken]).order_by(werken.c.werknummerID)
    elif keuze == 2 and validZt.zt(zoekterm, 8):
        sel = select([werken]).where(werken.c.werknummerID == int(zoekterm))
    elif keuze == 3:
        sel = select([werken]).where(werken.c.werkomschrijving.ilike('%'+zoekterm+'%'))
    elif keuze == 4 and validZt.zt(zoekterm, 18):
        sel = select([werken]).where(werken.c.voortgangstatus == zoekterm.upper())
    elif keuze == 5 and validZt.zt(zoekterm, 14):
        sel = select([werken]).where(werken.c.aanneemsom > float(zoekterm))
    elif keuze == 6 and validZt.zt(zoekterm, 14):
        sel = select([werken]).where(werken.c.aanneemsom < float(zoekterm))
    elif keuze == 7 and validZt.zt(zoekterm, 14):
        sel = select([werken]).where(werken.c.betaald_bedrag/werken.c.aanneemsom > float(zoekterm)/100)
    else:
        ongInvoer()
        werkenKeuze(m_email)
    
    if con.execute(sel).fetchone():
        rpwerken = con.execute(sel)
    else:
        geenRecord()
        werkenKeuze(m_email)
    
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1800, 900)
            self.setWindowTitle('Werken extern opvragen')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(showWerk)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            if not index.isValid():
                return None
            elif role != Qt.DisplayRole:
                return None
            return str(self.mylist[index.row()][index.column()]).format({'12.2f'})
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
  
    header = ['Werknummer','Werkomschrijving', 'Voortgangstatus','Statusweek',\
              'Startweek','Opdrachtdatum','Aanneemsom','Betaald bedrag','Begr.Materialen',\
              'Werk.Materialen', 'Begr.Lonen', 'Werk.Lonen', 'Begr.Materieel',\
              'Werk.materieel','Begr.leiding', 'Werk.leiding','Begr.huisvesting',\
              'Werk.huisvesting', 'Begr.inhuur','Werk.inhuur','Begr.Overig',\
              'Werk.Overig', 'Begr.Vervoer', 'Werk.Vervoer', 'Begr.beton bvl',\
              'Werk.beton bvl','Begr.kabelwerk', 'Werk.kabelwerk','Begr.grondverzet',\
              'Werk,grondverzet', 'Meerminderwerk','Begr.constr.uren','Werk.constr.uren',\
              'Begr.mont.uren', 'Werk.mont.uren', 'Begr.retourl.uren', 'Werk.retourl.uren',\
              'Begr.telecomuren','Werk.telecomuren', 'Begr.bfi-uren','Werk.bfi-uren',\
              'Begr.bvl-uren', 'Werk.bvl-uren','Begr.voedings-uren','Werk.voedings-uren',\
              'Begr.spoorleg-uren','Werk.spoorleg-uren', 'Begr.spoorlas-uren',\
              'Werk.spoorlas-uren', 'Begr.reis-uren', 'Werk.reis-uren']
   
    data_list=[]
    for row in rpwerken:
        data_list += [(row)] 
     
    def showWerk(idx):
        mwerknr = idx.data()
        if idx.column() == 0:
            selwerk = select([werken]).where(werken.c.werknummerID == mwerknr) 
            rpwerk = con.execute(selwerk).first()
            msom = rpwerk[6]
            mtotopbr = rpwerk[6]+rpwerk[30]
            mbtot = rpwerk[8]+rpwerk[10]+rpwerk[12]+rpwerk[14]+rpwerk[16]+rpwerk[18]+\
              rpwerk[20]+rpwerk[22]+rpwerk[24]+rpwerk[26]+rpwerk[28]+rpwerk[30]
            mktotal=rpwerk[9]+rpwerk[11]+rpwerk[13]+rpwerk[15]+rpwerk[17]+rpwerk[19]+rpwerk[21]+rpwerk[23]\
             +rpwerk[25]+rpwerk[27]+rpwerk[29]
            mbderden = rpwerk[16]+rpwerk[18]+rpwerk[20]+rpwerk[22]+rpwerk[24]+rpwerk[26]+rpwerk[28]
            mkderden = rpwerk[17]+rpwerk[19]+rpwerk[21]+rpwerk[23]+rpwerk[25]+rpwerk[27]+rpwerk[29]                     
            mbetaald = rpwerk[7]
            mvgangst = rpwerk[2]
            mstatwk = rpwerk[3]
            mfact = 0
            flag = 0
            mwerknr = rpwerk[0]
            mmeerwerk = float(rpwerk[30])
            if mvgangst == 'A':
                if mktotal > 0:
                    mvgangst = 'B'
                    mstatwk = jaarweek()
                    flag = 1
            elif mvgangst == 'B':      
                if mktotal > msom/3:
                    mvgangst = 'C'
                    mstatwk = jaarweek()
                    flag = 1
            elif mvgangst == 'C':
                if mktotal > msom/2:
                    mvgangst = 'D'
                    mstatwk = jaarweek()
                    flag = 1
                mfact = msom/3-mbetaald
            elif mvgangst == 'D':
                if mktotal > msom/1.5:
                    mvgangst = 'E'
                    mstatwk = jaarweek()
                    flag = 1
                mfact = 0
            elif mvgangst == 'E':
                if mktotal >= msom:
                    mvgangst = 'F'
                    mstatwk = jaarweek()
                    flag = 1
                mfact = msom/1.5-mbetaald
            elif mvgangst == 'F':
                mfact = msom-mbetaald*0.9
            elif mvgangst == 'G':
                mfact = msom+mmeerwerk-mbetaald 
            if flag:
                werkupd = update(werken).where(werken.c.werknummerID == mwerknr)\
                    .values(statusweek = mstatwk, voortgangstatus = mvgangst)
                con.execute(werkupd)
            class Widget(QDialog):
                 def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Werken extern gegevens opvragen")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                                          
                    self.setFont(QFont('Arial', 10))
                       
                    q1Edit = QLineEdit(str(rpwerk[0]))
                    q1Edit.setFixedWidth(100)
                    q1Edit.setDisabled(True)
                    q1Edit.setFont(QFont("Arial",10))
                    
                    q2Edit = QLineEdit(str(rpwerk[1]))
                    q2Edit.setFixedWidth(400)
                    q2Edit.setDisabled(True)
                    q2Edit.setFont(QFont("Arial",10))
                        
                    q3Edit = QLineEdit(rpwerk[2])
                    q3Edit.setFixedWidth(20)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.setDisabled(True)
                    
                    q4Edit = QLineEdit(rpwerk[3])
                    q4Edit.setFixedWidth(100)
                    q4Edit.setFont(QFont("Arial",10))
                    q4Edit.setDisabled(True)
           
                    q5Edit = QLineEdit(rpwerk[4])
                    q5Edit.setFixedWidth(100)
                    q5Edit.setFont(QFont("Arial",10))
                    q5Edit.setDisabled(True)                              
                    
                    q8Edit = QLineEdit(str(round(rpwerk[6],2)))
                    q8Edit.setFixedWidth(100)
                    q8Edit.setFont(QFont("Arial",10))
                    q8Edit.setDisabled(True)
                    
                    q9Edit = QLineEdit(str(round(rpwerk[30],2)))
                    q9Edit.setFixedWidth(100)
                    q9Edit.setFont(QFont("Arial",10))
                    q9Edit.setDisabled(True)
                                                         
                    q11Edit = QLineEdit(str(round(rpwerk[7],2)))
                    q11Edit.setFixedWidth(100)
                    q11Edit.setFont(QFont("Arial",10))
                    q11Edit.setDisabled(True)
                      
                    q12Edit = QLineEdit(str(round(rpwerk[8],2)))
                    q12Edit.setFixedWidth(100)
                    q12Edit.setFont(QFont("Arial",10))
                    q12Edit.setDisabled(True)
                     
                    q13Edit = QLineEdit(str(round(rpwerk[9],2)))
                    q13Edit.setFixedWidth(100)
                    q13Edit.setFont(QFont("Arial",10))
                    q13Edit.setDisabled(True)
             
                    q19Edit = QLineEdit(str(round(rpwerk[10],2)))
                    q19Edit.setFixedWidth(100)
                    q19Edit.setFont(QFont("Arial",10))
                    q19Edit.setDisabled(True)
             
                    q14Edit = QLineEdit(str(round(rpwerk[11],2)))
                    q14Edit.setFixedWidth(100)
                    q14Edit.setFont(QFont("Arial",10))
                    q14Edit.setDisabled(True)
                                    
                    q15Edit = QLineEdit(str(round(rpwerk[12],2)))
                    q15Edit.setDisabled(True)
                    q15Edit.setFixedWidth(100)
                    q15Edit.setFont(QFont("Arial",10))
                   
                    q16Edit = QLineEdit(str(round(rpwerk[13],2)))
                    q16Edit.setFixedWidth(100)
                    q16Edit.setFont(QFont("Arial",10))
                    q16Edit.setDisabled(True)
                        
                    q18Edit = QLineEdit(str(round(rpwerk[14],2)))
                    q18Edit.setFixedWidth(100)
                    q18Edit.setFont(QFont("Arial",10))
                    q18Edit.setDisabled(True)
                    
                    q17Edit = QLineEdit(str(round(rpwerk[15],2)))
                    q17Edit.setFixedWidth(100)
                    q17Edit.setFont(QFont("Arial",10))
                    q17Edit.setDisabled(True)
                    
                    q20Edit = QLineEdit(str(round(mtotopbr,2)))
                    q20Edit.setFixedWidth(100)
                    q20Edit.setFont(QFont("Arial",10))
                    q20Edit.setDisabled(True)
                    
                    q21Edit = QLineEdit(str(round(mbtot,2)))
                    q21Edit.setFixedWidth(100)
                    q21Edit.setFont(QFont("Arial",10))
                    q17Edit.setDisabled(True)
    
                    q22Edit = QLineEdit(str(round(mktotal,2)))
                    q22Edit.setFixedWidth(100)
                    q22Edit.setFont(QFont("Arial",10))
                    q22Edit.setDisabled(True)
    
                    q23Edit = QLineEdit(str(round(mbderden,2)))
                    q23Edit.setFixedWidth(100)
                    q23Edit.setFont(QFont("Arial",10))
                    q23Edit.setDisabled(True)
                    
                    q24Edit = QLineEdit(str(round(mkderden,2)))
                    q24Edit.setFixedWidth(100)
                    q24Edit.setFont(QFont("Arial",10))
                    q24Edit.setDisabled(True)
                                                  
                    q26Edit = QLineEdit(str(round(mfact,2)))
                    q26Edit.setFixedWidth(100)
                    q26Edit.setFont(QFont("Arial",10))
                    q26Edit.setDisabled(True)
                    
                    u1Edit = QLineEdit(str(round(rpwerk[31],2)))
                    u1Edit.setFixedWidth(100)
                    u1Edit.setFont(QFont("Arial",10))
                    u1Edit.setDisabled(True)
                    
                    u2Edit = QLineEdit(str(round(rpwerk[32],2)))
                    u2Edit.setFixedWidth(100)
                    u2Edit.setFont(QFont("Arial",10))
                    u2Edit.setDisabled(True)
                    
                    u3Edit = QLineEdit(str(round(rpwerk[33],2)))
                    u3Edit.setFixedWidth(100)
                    u3Edit.setFont(QFont("Arial",10))
                    u3Edit.setDisabled(True)
                    
                    u4Edit = QLineEdit(str(round(rpwerk[34],2)))
                    u4Edit.setFixedWidth(100)
                    u4Edit.setFont(QFont("Arial",10))
                    u4Edit.setDisabled(True)
                    
                    u5Edit = QLineEdit(str(round(rpwerk[35],2)))
                    u5Edit.setFixedWidth(100)
                    u5Edit.setFont(QFont("Arial",10))
                    u5Edit.setDisabled(True)
                    
                    u6Edit = QLineEdit(str(round(rpwerk[36],2)))
                    u6Edit.setFixedWidth(100)
                    u6Edit.setFont(QFont("Arial",10))
                    u6Edit.setDisabled(True)
                    
                    u7Edit = QLineEdit(str(round(rpwerk[37],2)))
                    u7Edit.setFixedWidth(100)
                    u7Edit.setFont(QFont("Arial",10))
                    u7Edit.setDisabled(True)
                    
                    u8Edit = QLineEdit(str(round(rpwerk[38],2)))
                    u8Edit.setFixedWidth(100)
                    u8Edit.setFont(QFont("Arial",10))
                    u8Edit.setDisabled(True)
                    
                    u9Edit = QLineEdit(str(round(rpwerk[39],2)))
                    u9Edit.setFixedWidth(100)
                    u9Edit.setFont(QFont("Arial",10))
                    u9Edit.setDisabled(True)
                    
                    u10Edit = QLineEdit(str(round(rpwerk[40],2)))
                    u10Edit.setFixedWidth(100)
                    u10Edit.setFont(QFont("Arial",10))
                    u10Edit.setDisabled(True)
                    
                    u11Edit = QLineEdit(str(round(rpwerk[41],2)))
                    u11Edit.setFixedWidth(100)
                    u11Edit.setFont(QFont("Arial",10))
                    u11Edit.setDisabled(True)
                    
                    u12Edit = QLineEdit(str(round(rpwerk[42],2)))
                    u12Edit.setFixedWidth(100)
                    u12Edit.setFont(QFont("Arial",10))
                    u12Edit.setDisabled(True)
                    
                    u13Edit = QLineEdit(str(round(rpwerk[43],2)))
                    u13Edit.setFixedWidth(100)
                    u13Edit.setFont(QFont("Arial",10))
                    u13Edit.setDisabled(True)
                    
                    u14Edit = QLineEdit(str(round(rpwerk[44],2)))
                    u14Edit.setFixedWidth(100)
                    u14Edit.setFont(QFont("Arial",10))
                    u14Edit.setDisabled(True)
                    
                    u15Edit = QLineEdit(str(round(rpwerk[45],2)))
                    u15Edit.setFixedWidth(100)
                    u15Edit.setFont(QFont("Arial",10))
                    u15Edit.setDisabled(True)
                    
                    u16Edit = QLineEdit(str(round(rpwerk[46],2)))
                    u16Edit.setFixedWidth(100)
                    u16Edit.setFont(QFont("Arial",10))
                    u16Edit.setDisabled(True)
                    
                    u17Edit = QLineEdit(str(round(rpwerk[47],2)))
                    u17Edit.setFixedWidth(100)
                    u17Edit.setFont(QFont("Arial",10))
                    u17Edit.setDisabled(True)
                    
                    u18Edit = QLineEdit(str(round(rpwerk[48],2)))
                    u18Edit.setFixedWidth(100)
                    u18Edit.setFont(QFont("Arial",10))
                    u18Edit.setDisabled(True)
                    
                    u19Edit = QLineEdit(str(round(rpwerk[49],2)))
                    u19Edit.setFixedWidth(100)
                    u19Edit.setFont(QFont("Arial",10))
                    u19Edit.setDisabled(True)
                    
                    u20Edit = QLineEdit(str(round(rpwerk[50],2)))
                    u20Edit.setFixedWidth(100)
                    u20Edit.setFont(QFont("Arial",10))
                    u20Edit.setDisabled(True)
                    
                    d1Edit = QLineEdit(str(round(rpwerk[16],2)))
                    d1Edit.setFixedWidth(100)
                    d1Edit.setFont(QFont("Arial",10))
                    d1Edit.setDisabled(True)
                                          
                    d2Edit = QLineEdit(str(round(rpwerk[17],2)))
                    d2Edit.setFixedWidth(100)
                    d2Edit.setFont(QFont("Arial",10))
                    d2Edit.setDisabled(True)
                    
                    d3Edit = QLineEdit(str(round(rpwerk[18],2)))
                    d3Edit.setFixedWidth(100)
                    d3Edit.setFont(QFont("Arial",10))
                    d3Edit.setDisabled(True)
                    
                    d4Edit = QLineEdit(str(round(rpwerk[19],2)))
                    d4Edit.setFixedWidth(100)
                    d4Edit.setFont(QFont("Arial",10))
                    d4Edit.setDisabled(True)
                    
                    d5Edit = QLineEdit(str(round(rpwerk[20],2)))
                    d5Edit.setFixedWidth(100)
                    d5Edit.setFont(QFont("Arial",10))
                    d5Edit.setDisabled(True)
                    
                    d6Edit = QLineEdit(str(round(rpwerk[21],2)))
                    d6Edit.setFixedWidth(100)
                    d6Edit.setFont(QFont("Arial",10))
                    d6Edit.setDisabled(True)
                    
                    d7Edit = QLineEdit(str(round(rpwerk[22],2)))
                    d7Edit.setFixedWidth(100)
                    d7Edit.setFont(QFont("Arial",10))
                    d7Edit.setDisabled(True)
                    
                    d8Edit = QLineEdit(str(round(rpwerk[23],2)))
                    d8Edit.setFixedWidth(100)
                    d8Edit.setFont(QFont("Arial",10))
                    d8Edit.setDisabled(True)
                    
                    d9Edit = QLineEdit(str(round(rpwerk[24],2)))
                    d9Edit.setFixedWidth(100)
                    d9Edit.setFont(QFont("Arial",10))
                    d9Edit.setDisabled(True)
                    
                    d10Edit = QLineEdit(str(round(rpwerk[25],2)))
                    d10Edit.setFixedWidth(100)
                    d10Edit.setFont(QFont("Arial",10))
                    d10Edit.setDisabled(True)
                    
                    d11Edit = QLineEdit(str(round(rpwerk[26],2)))
                    d11Edit.setFixedWidth(100)
                    d11Edit.setFont(QFont("Arial",10))
                    d11Edit.setDisabled(True)
                    
                    d12Edit = QLineEdit(str(round(rpwerk[27],2)))
                    d12Edit.setFixedWidth(100)
                    d12Edit.setFont(QFont("Arial",10))
                    d12Edit.setDisabled(True)
                    
                    d13Edit = QLineEdit(str(round(rpwerk[28],2)))
                    d13Edit.setFixedWidth(100)
                    d13Edit.setFont(QFont("Arial",10))
                    d13Edit.setDisabled(True)
                    
                    d14Edit = QLineEdit(str(round(rpwerk[29],2)))
                    d14Edit.setFixedWidth(100)
                    d14Edit.setFont(QFont("Arial",10))
                    d14Edit.setDisabled(True)
                                                  
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl ,0 , 0)
                    
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 8, 1, 1, Qt.AlignRight)
            
                    self.setFont(QFont('Arial', 10))
                    
                    grid.addWidget(QLabel('Werknummer'), 1, 0)
                    grid.addWidget(q1Edit, 1, 1) 
                    
                    grid.addWidget(QLabel('Werkomschrijving'), 1, 2)
                    grid.addWidget(q2Edit, 1, 3, 1, 3) 
                                                        
                    grid.addWidget(QLabel('Voortgangstatus'), 1, 6)
                    grid.addWidget(q3Edit, 1, 7)
                    
                    grid.addWidget(QLabel('Statusweek'), 1, 7, 1, 1, Qt.AlignRight)
                    grid.addWidget(q4Edit, 1, 8) 
                     
                    grid.addWidget(QLabel('Startweek'), 2, 2)
                    grid.addWidget(q5Edit, 2, 3)
                                                              
                    grid.addWidget(QLabel('Aanneemsom'), 2, 4)
                    grid.addWidget(q8Edit, 2, 5)
                    
                    grid.addWidget(QLabel('Meerminderwerk'), 2, 6)
                    grid.addWidget(q9Edit, 2,7)
                          
                    lbl1 = QLabel('Financieële totaal bedragen')
                    lbl1.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl1, 3, 0, 1, 2)
                    
                    grid.addWidget(QLabel('Totaal opbrengsten'), 4, 0)
                    grid.addWidget(q21Edit, 4, 1)
                    
                    grid.addWidget(QLabel('Totaal kosten'), 4, 2)
                    grid.addWidget(q22Edit, 4, 3)
                    
                    grid.addWidget(QLabel('Betaald bedrag'), 4, 4)
                    grid.addWidget(q11Edit, 4, 5)
                    
                    grid.addWidget(QLabel('Te factureren'), 4,  6)
                    grid.addWidget(q26Edit, 4, 7)
                    
                    grid.addWidget(QLabel('Begroot'), 5, 1)
                    grid.addWidget(QLabel('Werkelijk'), 5, 2)
                    grid.addWidget(QLabel('Begroot'), 5, 4)
                    grid.addWidget(QLabel('Werkelijk'), 5, 5)
                    grid.addWidget(QLabel('Begroot'), 5, 7)
                    grid.addWidget(QLabel('Werkelijk'), 5, 8)
           
                    grid.addWidget(QLabel('Materialen'), 6, 0)
                    grid.addWidget(q12Edit, 6, 1) 
                    grid.addWidget(q13Edit, 6, 2) 
                    
                    grid.addWidget(QLabel('Lonen'), 6, 3)
                    grid.addWidget(q19Edit, 6, 4)
                    grid.addWidget(q14Edit, 6, 5)
                                                
                    grid.addWidget(QLabel('Materieel'), 6, 6)
                    grid.addWidget(q15Edit, 6, 7)                           
                    grid.addWidget(q16Edit, 6, 8)
                    
                    grid.addWidget(QLabel('Derden'), 7, 0)
                    grid.addWidget(q23Edit, 7, 1)
                    grid.addWidget(q24Edit, 7, 2)
                     
                    grid.addWidget(QLabel('Leiding'), 7, 3)
                    grid.addWidget(q18Edit, 7, 4) 
                    grid.addWidget(q17Edit, 7,5) 
                        
                    lbl2 = QLabel('Werkuren verbruik')
                    lbl2.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl2, 8, 0, 1, 2)
                    
                    grid.addWidget(QLabel('Begroot'), 9, 1)
                    grid.addWidget(QLabel('Werkelijk'), 9, 2)
                    grid.addWidget(QLabel('Begroot'), 9, 4)
                    grid.addWidget(QLabel('Werkelijk'), 9, 5) 
                    grid.addWidget(QLabel('Begroot'), 9, 7)
                    grid.addWidget(QLabel('Werkelijk'), 9, 8)  
                    
                    grid.addWidget(QLabel('Construktie'), 10, 0)
                    grid.addWidget(u1Edit, 10,1)
                    grid.addWidget(u2Edit, 10,2) 

                    grid.addWidget(QLabel('Montage'), 10, 3)
                    grid.addWidget(u3Edit, 10,4)
                    grid.addWidget(u4Edit, 10,5) 
                    
                    grid.addWidget(QLabel('Retourlas'), 10, 6)
                    grid.addWidget(u5Edit, 10,7)
                    grid.addWidget(u6Edit, 10,8) 
                    
                    grid.addWidget(QLabel('Telecom'), 11, 0)
                    grid.addWidget(u7Edit, 11,1)
                    grid.addWidget(u8Edit, 11,2) 
                    
                    grid.addWidget(QLabel('Bfi'), 11, 3)
                    grid.addWidget(u9Edit, 11,4)
                    grid.addWidget(u10Edit, 11,5)
                    
                    grid.addWidget(QLabel('Bovenleiding'), 11, 6)
                    grid.addWidget(u11Edit, 11,7)
                    grid.addWidget(u12Edit, 11,8)
                    
                    grid.addWidget(QLabel('Voeding'), 12, 0)
                    grid.addWidget(u13Edit, 12,1)
                    grid.addWidget(u14Edit, 12,2)
                    
                    grid.addWidget(QLabel('Spoorleg'), 12, 3)
                    grid.addWidget(u15Edit, 12,4)
                    grid.addWidget(u16Edit, 12,5)
                    
                    grid.addWidget(QLabel('Spoorlas'), 12, 6)
                    grid.addWidget(u17Edit, 12,7)
                    grid.addWidget(u18Edit, 12,8)
                    
                    grid.addWidget(QLabel('Reisuren'), 13, 0)
                    grid.addWidget(u19Edit, 13,1)
                    grid.addWidget(u20Edit, 13,2)
                    
                    lbl3 = QLabel('Diensten derden')
                    lbl3.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl3, 14, 0, 1, 2)
                    
                    grid.addWidget(QLabel('Begroot'), 15, 1)
                    grid.addWidget(QLabel('Werkelijk'), 15, 2)
                    grid.addWidget(QLabel('Begroot'), 15, 4)
                    grid.addWidget(QLabel('Werkelijk'), 15, 5) 
                    grid.addWidget(QLabel('Begroot'), 15, 7)
                    grid.addWidget(QLabel('Werkelijk'), 15, 8)  
                      
                    grid.addWidget(QLabel('Huisvesting'), 16, 0)
                    grid.addWidget(d1Edit, 16,1)
                    grid.addWidget(d2Edit, 16,2)
                    
                    grid.addWidget(QLabel('Inhuur'), 16, 3)
                    grid.addWidget(d3Edit, 16,4)
                    grid.addWidget(d4Edit, 16,5)
                    
                    grid.addWidget(QLabel('Overig'), 16, 6)
                    grid.addWidget(d5Edit, 16,7)
                    grid.addWidget(d6Edit, 16,8)
                    
                    grid.addWidget(QLabel('Vervoer'), 17, 0)
                    grid.addWidget(d7Edit, 17,1)
                    grid.addWidget(d8Edit, 17,2)
                    
                    grid.addWidget(QLabel('Beton bvl'), 17, 3)
                    grid.addWidget(d9Edit, 17,4)
                    grid.addWidget(d10Edit, 17,5)
                    
                    grid.addWidget(QLabel('Kabelwerk'), 17, 6)
                    grid.addWidget(d11Edit, 17,7)
                    grid.addWidget(d12Edit, 17,8)
                    
                    grid.addWidget(QLabel('Grondverzet'), 18, 0)
                    grid.addWidget(d13Edit, 18,1)
                    grid.addWidget(d14Edit, 18,2)
                     
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 20, 0, 1, 8, Qt.AlignCenter)
                    self.setLayout(grid)
                    self.setGeometry(400, 50, 350, 300)
                                                                            
                    cancelBtn = QPushButton('Sluiten')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 19, 8, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            window = Widget()
            window.exec_() 
                       
    win = MyWindow(data_list, header)
    win.exec_()
    werkenKeuze(m_email)  