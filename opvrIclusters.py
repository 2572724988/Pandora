from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout, QComboBox,\
    QDialog, QLabel, QGridLayout, QPushButton, QMessageBox, QLineEdit
from sqlalchemy import (Table, Column, String, Float, MetaData,\
                         create_engine)
from sqlalchemy.sql import select

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Iclusters opvragen')               
    msg.exec_() 
 
def windowSluit(self,m_email):
    self.close()
    hoofdMenu(m_email)
   
def ongKeuze():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Ongeldige keuze')
    msg.setWindowTitle('Clusters invoeren')               
    msg.exec_() 

def zoeken(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Cluster selektie")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                              
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(340)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: gainsboro")
            k0Edit.addItem('              Sorteersleutel Clustergroepen')
            k0Edit.addItem('0. Alle Clusters')
            k0Edit.addItem('LA-LK. Bewerkte onderdelen')
            k0Edit.addItem('MA-MK. Bouten en Moeren')
            k0Edit.addItem('NA-NK. Gietwerk bewerking')
            k0Edit.addItem('OA-OK. Laswerk samengesteld')
            k0Edit.addItem('PA-PK. Plaatwerk samengesteld')
            k0Edit.addItem('RA-RK. Kunstof onderdelen')
            k0Edit.addItem('SA-SK. Prefab Montagedelen')
            k0Edit.addItem('TA-TK. Samengestelde Onderdelen')
            k0Edit.activated[str].connect(self.k0Changed)
      
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                        
            grid.addWidget(k0Edit, 1, 0, 1, 2, Qt.AlignRight)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 3, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
   
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 2, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self,m_email))
    
            grid.addWidget(cancelBtn, 2, 0, 1 , 2, Qt.AlignCenter)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
           
        def k0Changed(self, text):
            self.Keuze.setText(text)
         
        def returnk0(self):
            return self.Keuze.text()
               
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0()]       

    window = Widget()
    data = window.getData()
    keuze = ''
    if not data[0]:
        ongKeuze()
        zoeken(m_email)
    elif data[0][0] == '0':
        keuze = ''
    elif data[0]:
        keuze = data[0][0]
    toonIclusters(keuze, m_email)

def toonIclusters(keuze, m_email):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1700, 900)
            self.setWindowTitle('Intern Cluster Calculatie')
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
            table_view.clicked.connect(showSelection)
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
            return str(self.mylist[index.row()][index.column()])
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
             
    header = ['Clusternr','Omschrijving','Prijs','Eenheid','Materialen','Lonen',\
              'Diensten','Materiëel','Inhuur','St.zagen','Zagen','St.schaven','Schaven',\
              'St.steken','Steken','St.boren','Boren','St.frezen','Frezen','St.draaien klein',\
              'Draaien klein','St.draaien_groot','Draaien groot','St.tappen','Tappen',\
              'St.nube draaien','Nube draaien','St.nube bewerken','Nube bewerken',\
              'St.knippen','Knippen','St.kanten','Kanten','St.stansen','Stansen',\
              'St.lassen co2','Lassen co2','St.lassen hand','Lassen hand','St.verpakken',\
              'Verpakken','St.verzinken','Verzinken','St.moffelen','Moffelen','St.schilderen',\
              'Schilderen','St.spuiten','Spuiten','St.ponsen','Ponsen','St.persen',\
              'Persen','St.gritstralen','Gritstralen','St.montage','Montage']
     
    metadata = MetaData()
    iclusters = Table('iclusters', metadata,
        Column('iclusterID', String, primary_key=True),
        Column('omschrijving', String),
        Column('prijs', Float),
        Column('eenheid', String),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('diensten', Float),
        Column('materieel', Float),
        Column('inhuur', Float),
        Column('szagen', Float),
        Column('zagen', Float),
        Column('sschaven', Float),
        Column('schaven', Float),
        Column('ssteken', Float),
        Column('steken', Float),
        Column('sboren', Float),
        Column('boren', Float),
        Column('sfrezen', Float),
        Column('frezen', Float),
        Column('sdraaien_klein', Float),
        Column('draaien_klein', Float),
        Column('sdraaien_groot', Float),
        Column('draaien_groot', Float),
        Column('stappen', Float),
        Column('tappen', Float),
        Column('snube_draaien', Float),
        Column('nube_draaien', Float),
        Column('snube_bewerken', Float),
        Column('nube_bewerken', Float),
        Column('sknippen', Float),
        Column('knippen', Float),
        Column('skanten', Float),
        Column('kanten', Float),
        Column('sstansen', Float),
        Column('stansen', Float),
        Column('slassen_co2', Float),
        Column('lassen_co2', Float),
        Column('slassen_hand', Float),
        Column('lassen_hand', Float),
        Column('sverpakken', Float),
        Column('verpakken', Float),
        Column('sverzinken', Float),
        Column('verzinken', Float),
        Column('smoffelen', Float),
        Column('moffelen', Float),
        Column('sschilderen', Float),
        Column('schilderen', Float),
        Column('sspuiten', Float),
        Column('spuiten', Float),
        Column('sponsen', Float),
        Column('ponsen', Float),
        Column('spersen', Float),
        Column('persen', Float),
        Column('sgritstralen', Float),
        Column('gritstralen', Float),
        Column('smontage', Float),
        Column('montage', Float))
               
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
        
    sel = select([iclusters]).where(iclusters.c.iclusterID.ilike(keuze+'%'))\
                              .order_by(iclusters.c.iclusterID)
       
    if con.execute(sel).fetchone():
        rp = con.execute(sel)
    else:
        geenRecord()
        zoeken(m_email)
     
    data_list=[]
    for row in rp:
        data_list += [(row)]
        
    def showSelection(idx):
        clusternr = idx.data()
        if idx.column() == 0:
 
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selcl = select([iclusters]).where(iclusters.c.iclusterID == clusternr)
            rpsel = con.execute(selcl).first()
            
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    self.setWindowTitle("Opvragen Cluster")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
  
                    self.Omschrijving = QLabel()
                    q1Edit = QLineEdit(rpsel[1])
                    q1Edit.setFixedWidth(400)
                    q1Edit.setFont(QFont("Arial",10))
                    q1Edit.setDisabled(True)
                                    
                    self.Prijs = QLabel()
                    q2Edit = QLineEdit(str(round(rpsel[2],2)))
                    q2Edit.setFixedWidth(150)
                    q2Edit.setFont(QFont("Arial",10))
                    q2Edit.setDisabled(True)
                    
                    self.Eenheid = QLabel()
                    q3Edit = QLineEdit(str(rpsel[3]))
                    q3Edit.setFixedWidth(150)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.setDisabled(True)
                      
                    self.Materialen = QLabel()
                    q4Edit = QLineEdit(str(round(rpsel[4],2)))
                    q4Edit.setFixedWidth(150)
                    q4Edit.setFont(QFont("Arial",10))
                    q4Edit.setDisabled(True)
                    
                    self.Lonen = QLabel()
                    q5Edit = QLineEdit(str(round(rpsel[5],2)))
                    q5Edit.setFixedWidth(150)
                    q5Edit.setFont(QFont("Arial",10))
                    q5Edit.setDisabled(True)
                    
                    self.Diensten = QLabel()
                    q6Edit = QLineEdit(str(round(rpsel[6],2)))
                    q6Edit.setFixedWidth(150)
                    q6Edit.setFont(QFont("Arial",10))
                    q6Edit.setDisabled(True)
                    
                    self.Materiëel = QLabel()
                    q7Edit = QLineEdit(str(round(rpsel[7],2)))
                    q7Edit.setFixedWidth(150)
                    q7Edit.setFont(QFont("Arial",10))
                    q7Edit.setDisabled(True)
                    
                    self.Inhuur = QLabel()
                    q8Edit = QLineEdit(str(round(rpsel[8],2)))
                    q8Edit.setFixedWidth(150)
                    q8Edit.setFont(QFont("Arial",10))
                    q8Edit.setDisabled(True)
                      
                    self.Szagen = QLabel()
                    q9Edit = QLineEdit(str(rpsel[9]))
                    q9Edit.setFixedWidth(150)
                    q9Edit.setFont(QFont("Arial",10))
                    q9Edit.setDisabled(True)
                    
                    self.Zagen = QLabel()
                    q10Edit = QLineEdit(str(rpsel[10]))
                    q10Edit.setFixedWidth(150)
                    q10Edit.setFont(QFont("Arial",10))
                    q10Edit.setDisabled(True)
                    
                    self.Sschaven = QLabel()
                    q11Edit = QLineEdit(str(rpsel[11]))
                    q11Edit.setFixedWidth(150)
                    q11Edit.setFont(QFont("Arial",10))
                    q11Edit.setDisabled(True)
                    
                    self.Schaven = QLabel()
                    q12Edit = QLineEdit(str(rpsel[12]))
                    q12Edit.setFixedWidth(150)
                    q12Edit.setFont(QFont("Arial",10))
                    q12Edit.setDisabled(True)
                    
                    self.Ssteken = QLabel()
                    q13Edit = QLineEdit(str(rpsel[13]))
                    q13Edit.setFixedWidth(150)
                    q13Edit.setFont(QFont("Arial",10))
                    q13Edit.setDisabled(True)
                    
                    self.Steken = QLabel()
                    q14Edit = QLineEdit(str(rpsel[14]))
                    q14Edit.setFixedWidth(150)
                    q14Edit.setFont(QFont("Arial",10))
                    q14Edit.setDisabled(True)
                    
                    self.Sboren = QLabel()
                    q15Edit = QLineEdit(str(rpsel[15]))
                    q15Edit.setFixedWidth(150)
                    q15Edit.setFont(QFont("Arial",10))
                    q15Edit.setDisabled(True)
                                   
                    self.Boren = QLabel()
                    q16Edit = QLineEdit(str(rpsel[16]))
                    q16Edit.setFixedWidth(150)
                    q16Edit.setFont(QFont("Arial",10))
                    q16Edit.setDisabled(True)
                    
                    self.Sfrezen = QLabel()
                    q17Edit = QLineEdit(str(rpsel[17]))
                    q17Edit.setFixedWidth(150)
                    q17Edit.setFont(QFont("Arial",10))
                    q17Edit.setDisabled(True)
                    
                    self.Frezen = QLabel()
                    q18Edit = QLineEdit(str(rpsel[18]))
                    q18Edit.setFixedWidth(150)
                    q18Edit.setFont(QFont("Arial",10))
                    q18Edit.setDisabled(True)
                    
                    self.Sdraaien_klein = QLabel()
                    q19Edit = QLineEdit(str(rpsel[19]))
                    q19Edit.setFixedWidth(150)
                    q19Edit.setFont(QFont("Arial",10))
                    q19Edit.setDisabled(True)

                    self.Draaien_klein = QLabel()
                    q20Edit = QLineEdit(str(rpsel[20]))
                    q20Edit.setFixedWidth(150)
                    q20Edit.setFont(QFont("Arial",10))
                    q20Edit.setDisabled(True)
                    
                    self.SDraaien_groot = QLabel()
                    q21Edit = QLineEdit(str(rpsel[21]))
                    q21Edit.setFixedWidth(150)
                    q21Edit.setFont(QFont("Arial",10))
                    q21Edit.setDisabled(True)
                  
                    self.Draaien_groot = QLabel()
                    q22Edit = QLineEdit(str(rpsel[22]))
                    q22Edit.setFixedWidth(150)
                    q22Edit.setFont(QFont("Arial",10))
                    q22Edit.setDisabled(True)
                 
                    self.Stappen = QLabel()
                    q23Edit = QLineEdit(str(rpsel[23]))
                    q23Edit.setFixedWidth(150)
                    q23Edit.setFont(QFont("Arial",10))
                    q23Edit.setDisabled(True)
                       
                    self.Tappen = QLabel()
                    q24Edit = QLineEdit(str(rpsel[24]))
                    q24Edit.setFixedWidth(150)
                    q24Edit.setFont(QFont("Arial",10))
                    q24Edit.setDisabled(True)
                    
                    self.Snube_draaien = QLabel()
                    q25Edit = QLineEdit(str(rpsel[25]))
                    q25Edit.setFixedWidth(150)
                    q25Edit.setFont(QFont("Arial",10))
                    q25Edit.setDisabled(True)
                    
                    self.Nube_draaien = QLabel()
                    q26Edit = QLineEdit(str(rpsel[26]))
                    q26Edit.setFixedWidth(150)
                    q26Edit.setFont(QFont("Arial",10))
                    q26Edit.setDisabled(True)
                    
                    self.Snube_bewerken = QLabel()
                    q27Edit = QLineEdit(str(rpsel[27]))
                    q27Edit.setFixedWidth(150)
                    q27Edit.setFont(QFont("Arial",10))
                    q27Edit.setDisabled(True)

                    self.Nube_bewerken = QLabel()
                    q28Edit = QLineEdit(str(rpsel[28]))
                    q28Edit.setFixedWidth(150)
                    q28Edit.setFont(QFont("Arial",10))
                    q28Edit.setDisabled(True)
                    
                    self.Sknippen = QLabel()
                    q29Edit = QLineEdit(str(rpsel[29]))
                    q29Edit.setFixedWidth(150)
                    q29Edit.setFont(QFont("Arial",10))
                    q29Edit.setDisabled(True)
                       
                    self.Knippen = QLabel()
                    q30Edit = QLineEdit(str(rpsel[30]))
                    q30Edit.setFixedWidth(150)
                    q30Edit.setFont(QFont("Arial",10))
                    q30Edit.setDisabled(True)
                    
                    self.Skanten = QLabel()
                    q31Edit = QLineEdit(str(rpsel[31]))
                    q31Edit.setFixedWidth(150)
                    q31Edit.setFont(QFont("Arial",10))
                    q31Edit.setDisabled(True)
                            
                    self.Kanten = QLabel()
                    q32Edit = QLineEdit(str(rpsel[32]))
                    q32Edit.setFixedWidth(150)
                    q32Edit.setFont(QFont("Arial",10))
                    q32Edit.setDisabled(True)

                    self.Sstansen = QLabel()
                    q33Edit = QLineEdit(str(rpsel[33]))
                    q33Edit.setFixedWidth(150)
                    q33Edit.setFont(QFont("Arial",10))
                    q33Edit.setDisabled(True)
                    
                    self.Stansen = QLabel()
                    q34Edit = QLineEdit(str(rpsel[34]))
                    q34Edit.setFixedWidth(150)
                    q34Edit.setFont(QFont("Arial",10))
                    q34Edit.setDisabled(True)
                    
                    self.Slassen_CO2 = QLabel()
                    q35Edit = QLineEdit(str(rpsel[35]))
                    q35Edit.setFixedWidth(150)
                    q35Edit.setFont(QFont("Arial",10))
                    q35Edit.setDisabled(True)
                    
                    self.Lassen_CO2 = QLabel()
                    q36Edit = QLineEdit(str(rpsel[36]))
                    q36Edit.setFixedWidth(150)
                    q36Edit.setFont(QFont("Arial",10))
                    q36Edit.setDisabled(True)

                    self.Slassen_hand = QLabel()
                    q37Edit = QLineEdit(str(rpsel[37]))
                    q37Edit.setFixedWidth(150)
                    q37Edit.setFont(QFont("Arial",10))
                    q37Edit.setDisabled(True)
                    
                    self.Lassen_hand = QLabel()
                    q38Edit = QLineEdit(str(rpsel[38]))
                    q38Edit.setFixedWidth(150)
                    q38Edit.setFont(QFont("Arial",10))
                    q38Edit.setDisabled(True)
                    
                    self.Sverpakken = QLabel()
                    q39Edit = QLineEdit(str(rpsel[39]))
                    q39Edit.setFixedWidth(150)
                    q39Edit.setFont(QFont("Arial",10))
                    q39Edit.setDisabled(True)                    
                     
                    self.Verpakken = QLabel()
                    q40Edit = QLineEdit(str(rpsel[40]))
                    q40Edit.setFixedWidth(150)
                    q40Edit.setFont(QFont("Arial",10))
                    q40Edit.setDisabled(True)
                                        
                    self.Sverzinken = QLabel()
                    q41Edit = QLineEdit(str(rpsel[41]))
                    q41Edit.setFixedWidth(150)
                    q41Edit.setFont(QFont("Arial",10))
                    q41Edit.setDisabled(True)
                                        
                    self.Verzinken = QLabel()
                    q42Edit = QLineEdit(str(rpsel[42]))
                    q42Edit.setFixedWidth(150)
                    q42Edit.setFont(QFont("Arial",10))
                    q42Edit.setDisabled(True)

                    self.Smoffelen = QLabel()
                    q43Edit = QLineEdit(str(rpsel[43]))
                    q43Edit.setFixedWidth(150)
                    q43Edit.setFont(QFont("Arial",10))
                    q43Edit.setDisabled(True)
                   
                    self.Moffelen = QLabel()
                    q44Edit = QLineEdit(str(rpsel[44]))
                    q44Edit.setFixedWidth(150)
                    q44Edit.setFont(QFont("Arial",10))
                    q44Edit.setDisabled(True)
                    
                    self.Sschilderen = QLabel()
                    q45Edit = QLineEdit(str(rpsel[45]))
                    q45Edit.setFixedWidth(150)
                    q45Edit.setFont(QFont("Arial",10))
                    q45Edit.setDisabled(True)
                    
                    self.Schilderen = QLabel()
                    q46Edit = QLineEdit(str(rpsel[46]))
                    q46Edit.setFixedWidth(150)
                    q46Edit.setFont(QFont("Arial",10))
                    q46Edit.setDisabled(True)
                    
                    self.Sspuiten = QLabel()
                    q47Edit = QLineEdit(str(rpsel[47]))
                    q47Edit.setFixedWidth(150)
                    q47Edit.setFont(QFont("Arial",10))
                    q47Edit.setDisabled(True)
                    
                    self.Spuiten = QLabel()
                    q48Edit = QLineEdit(str(rpsel[48]))
                    q48Edit.setFixedWidth(150)
                    q48Edit.setFont(QFont("Arial",10))
                    q48Edit.setDisabled(True)
                    
                    self.Sponsen = QLabel()
                    q49Edit = QLineEdit(str(rpsel[49]))
                    q49Edit.setFixedWidth(150)
                    q49Edit.setFont(QFont("Arial",10))
                    q49Edit.setDisabled(True)
                    
                    self.Ponsen = QLabel()
                    q50Edit = QLineEdit(str(rpsel[50]))
                    q50Edit.setFixedWidth(150)
                    q50Edit.setFont(QFont("Arial",10))
                    q50Edit.setDisabled(True)
                    
                    self.Spersen = QLabel()
                    q51Edit = QLineEdit(str(rpsel[51]))
                    q51Edit.setFixedWidth(150)
                    q51Edit.setFont(QFont("Arial",10))
                    q51Edit.setDisabled(True)                    
                    
                    self.Persen = QLabel()
                    q52Edit = QLineEdit(str(rpsel[52]))
                    q52Edit.setFixedWidth(150)
                    q52Edit.setFont(QFont("Arial",10))
                    q52Edit.setDisabled(True) 

                    self.Sgritstralen = QLabel()
                    q53Edit = QLineEdit(str(rpsel[53]))
                    q53Edit.setFixedWidth(150)
                    q53Edit.setFont(QFont("Arial",10))
                    q53Edit.setDisabled(True) 
                    
                    self.Gritstralen = QLabel()
                    q54Edit = QLineEdit(str(rpsel[54]))
                    q54Edit.setFixedWidth(150)
                    q54Edit.setFont(QFont("Arial",10))
                    q54Edit.setDisabled(True) 
                    
                    self.Smontage = QLabel()
                    q55Edit = QLineEdit(str(rpsel[55]))
                    q55Edit.setFixedWidth(150)
                    q55Edit.setFont(QFont("Arial",10))
                    q55Edit.setDisabled(True) 
                                     
                    self.Montage = QLabel()
                    q56Edit = QLineEdit(str(rpsel[56]))
                    q56Edit.setFixedWidth(150)
                    q56Edit.setFont(QFont("Arial",10))
                    q56Edit.setDisabled(True)  
                                                                          
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl1 = QLabel('Clusternummer')  
                    lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl1, 1, 0)
                    
                    lbl2 = QLabel(clusternr)
                    grid.addWidget(lbl2, 1, 1)
                           
                    lbl3 = QLabel('Omschrijving')  
                    lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl3, 1, 2)
                    grid.addWidget(q1Edit, 1, 3, 1, 3) # RowSpan 1 ,ColumnSpan 3
                                                         
                    lbl4 = QLabel('Prijs')  
                    lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl4, 2, 0)
                    grid.addWidget(q2Edit, 2, 1)
                    
                    lbl5 = QLabel('Eenheid')  
                    lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl5, 2, 2)
                    grid.addWidget(q3Edit, 2, 3)
                    
                    lbl6 = QLabel('Materialen')  
                    lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl6, 2, 4)
                    grid.addWidget(q4Edit, 2, 5)
                    
                    lbl7 = QLabel('Lonen')  
                    lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl7, 2, 6)
                    grid.addWidget(q5Edit, 2, 7)
                    
                    lbl8 = QLabel('Diensten')  
                    lbl8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl8, 3, 0)
                    grid.addWidget(q6Edit, 3, 1)
                    
                    lbl9 = QLabel('Materiëel')  
                    lbl9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl9, 3, 2)
                    grid.addWidget(q7Edit, 3, 3)
                    
                    lbl10 = QLabel('Inhuur')  
                    lbl10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl10, 3, 4)
                    grid.addWidget(q8Edit, 3, 5)
                    
                    lbl11 = QLabel('St.zagen')  
                    lbl11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl11, 4, 0)
                    grid.addWidget(q9Edit, 4, 1)
                    
                    lbl12 = QLabel('Zagen')  
                    lbl12.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl12, 4, 2)
                    grid.addWidget(q10Edit, 4, 3)
                    
                    lbl13 = QLabel('St.schaven')  
                    lbl13.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl13, 4, 4)
                    grid.addWidget(q11Edit, 4, 5)
                      
                    lbl14 = QLabel('Schaven')  
                    lbl14.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl14, 4, 6)
                    grid.addWidget(q12Edit, 4, 7)
                    
                    lbl15 = QLabel('St.steken')  
                    lbl15.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl15, 5, 0)
                    grid.addWidget(q13Edit, 5, 1)
                    
                    lbl16 = QLabel('Steken')  
                    lbl16.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl16, 5, 2)
                    grid.addWidget(q14Edit, 5, 3)
                    
                    lbl17 = QLabel('St.boren')  
                    lbl17.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl17, 5, 4)
                    grid.addWidget(q15Edit, 5, 5)
                    
                    lbl18 = QLabel('Boren')  
                    lbl18.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl18, 5, 6)
                    grid.addWidget(q16Edit, 5, 7)
                    
                    lbl19 = QLabel('St.frezen')  
                    lbl19.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl19, 6, 0)
                    grid.addWidget(q17Edit, 6, 1)
                    
                    lbl20 = QLabel('Frezen')  
                    lbl20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl20, 6, 2)
                    grid.addWidget(q18Edit, 6, 3)
                    
                    lbl21 = QLabel('St.draaien-klein')  
                    lbl21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl21, 6, 4)
                    grid.addWidget(q19Edit, 6, 5)
                    
                    lbl22 = QLabel('Draaien-klein')  
                    lbl22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl22, 6, 6)
                    grid.addWidget(q20Edit, 6, 7)
                    
                    lbl23 = QLabel('St.draaien-groot')  
                    lbl23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl23, 7, 0)
                    grid.addWidget(q21Edit, 7, 1)
                    
                    lbl26 = QLabel('Draaien-groot')  
                    lbl26.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl26, 7, 2)
                    grid.addWidget(q22Edit, 7, 3)
                    
                    lbl27 = QLabel('St.tappen')  
                    lbl27.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl27, 7, 4)
                    grid.addWidget(q23Edit, 7, 5)
                    
                    lbl28 = QLabel('Tappen')  
                    lbl28.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl28, 7, 6)
                    grid.addWidget(q24Edit, 7, 7)
                    
                    lbl27 = QLabel('St.nube_draaien')  
                    lbl27.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl27, 8, 0)
                    grid.addWidget(q25Edit, 8, 1)
                    
                    lbl28 = QLabel('Nube_draaien')  
                    lbl28.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl28, 8, 2)
                    grid.addWidget(q26Edit, 8, 3)
                    
                    lbl29 = QLabel('St.nube-bewerken')  
                    lbl29.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl29, 8, 4)
                    grid.addWidget(q27Edit, 8, 5)
                    
                    lbl30 = QLabel('Nube-bewerken')  
                    lbl30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl30, 8, 6)
                    grid.addWidget(q28Edit, 8, 7)
                    
                    lbl31 = QLabel('St.knippen')  
                    lbl31.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl31, 9, 0)
                    grid.addWidget(q29Edit, 9, 1)
                    
                    lbl32 = QLabel('Knippen')  
                    lbl32.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl32, 9, 2)
                    grid.addWidget(q30Edit, 9, 3)
                    
                    lbl33 = QLabel('St.kanten')  
                    lbl33.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl33, 9, 4)
                    grid.addWidget(q31Edit, 9, 5)
                    
                    lbl34 = QLabel('Kanten')  
                    lbl34.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl34, 9, 6)
                    grid.addWidget(q32Edit, 9, 7)
                    
                    lbl35 = QLabel('St.stansen')  
                    lbl35.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl35, 10, 0)
                    grid.addWidget(q33Edit, 10, 1)
                    
                    lbl36 = QLabel('Stansen')  
                    lbl36.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl36, 10, 2)
                    grid.addWidget(q34Edit, 10, 3)
                    
                    lbl37 = QLabel('St.Lassen-Co2')  
                    lbl37.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl37, 10, 4)
                    grid.addWidget(q35Edit, 10, 5)
                    
                    lbl38 = QLabel('Lassen-Co2')  
                    lbl38.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl38, 10, 6)
                    grid.addWidget(q36Edit, 10, 7)
                    
                    lbl39 = QLabel('St.Lassen-hand')  
                    lbl39.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl39, 11, 0)
                    grid.addWidget(q37Edit, 11, 1)
                    
                    lbl40 = QLabel('Lassen-hand')  
                    lbl40.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl40, 11, 2)
                    grid.addWidget(q38Edit, 11, 3)
                    
                    lbl41 = QLabel('St.Verpakken')  
                    lbl41.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl41, 11, 4)
                    grid.addWidget(q39Edit, 11, 5)
                        
                    lbl42 = QLabel('Verpakken')  
                    lbl42.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl42, 11, 6)
                    grid.addWidget(q40Edit, 11, 7)
                    
                    lbl43 = QLabel('St.Verzinken')  
                    lbl43.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl43, 12, 0)
                    grid.addWidget(q41Edit, 12, 1)
                    
                    lbl44 = QLabel('Verzinken')  
                    lbl44.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl44, 12, 2)
                    grid.addWidget(q42Edit, 12, 3)
                    
                    lbl45 = QLabel('St.Moffelen')  
                    lbl45.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl45, 12, 4)
                    grid.addWidget(q43Edit, 12, 5)
                    
                    lbl46 = QLabel('Moffelen')  
                    lbl46.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl46, 12, 6)
                    grid.addWidget(q44Edit, 12, 7)
                    
                    lbl47 = QLabel('St.Schilderen')  
                    lbl47.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl47, 13, 0)
                    grid.addWidget(q45Edit, 13, 1)
                    
                    lbl48 = QLabel('Schilderen')  
                    lbl48.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl48, 13, 2)
                    grid.addWidget(q46Edit, 13, 3)
                    
                    lbl49 = QLabel('St.Spuiten')  
                    lbl49.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl49, 13, 4)
                    grid.addWidget(q47Edit, 13, 5)
                                                              
                    lbl50 = QLabel('Spuiten')  
                    lbl50.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl50, 13, 6)
                    grid.addWidget(q48Edit, 13, 7)
                    
                    lbl51 = QLabel('St.Ponsen')
                    lbl51.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl51, 14, 0)
                    grid.addWidget(q49Edit, 14, 1)
                 
                    lbl52 = QLabel('Ponsen')
                    lbl52.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl52, 14, 2)
                    grid.addWidget(q50Edit, 14, 3)
                    
                    lbl53 = QLabel('St.Persen')  
                    lbl53.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl53, 14, 4)
                    grid.addWidget(q51Edit, 14, 5)
                    
                    lbl54 = QLabel('Persen')  
                    lbl54.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl54, 14, 6)
                    grid.addWidget(q52Edit, 14, 7)
                    
                    lbl55 = QLabel('St.Gritstralen')  
                    lbl55.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl55, 15, 0)
                    grid.addWidget(q53Edit, 15, 1)
                    
                    lbl56 = QLabel('Gritstralen')  
                    lbl56.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl56, 15, 2)
                    grid.addWidget(q54Edit, 15, 3)
                    
                    lbl57 = QLabel('St.Montage')  
                    lbl57.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl57, 15, 4)
                    grid.addWidget(q55Edit, 15, 5)
                    
                    lbl58 = QLabel('Montage')  
                    lbl58.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    grid.addWidget(lbl58, 15, 6)
                    grid.addWidget(q56Edit, 15, 7)
                          
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl, 0, 0, 1, 1, Qt.AlignRight)
                                     
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 7, 1 , 1, Qt.AlignRight)
                    
                    grid.addWidget(QLabel('Opvragen interne clusters'), 0, 1, 1, 8, Qt.AlignCenter)
                                                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 18, 0, 1, 8, Qt.AlignCenter)
                    self.setLayout(grid)
                    self.setGeometry(300, 100, 150, 150)
            
                    sluitBtn = QPushButton('Sluiten')
                    sluitBtn.clicked.connect(self.close)
            
                    grid.addWidget(sluitBtn, 17, 7, 1, 1, Qt.AlignRight)
                    sluitBtn.setFont(QFont("Arial",10))
                    sluitBtn.setFixedWidth(100)
                    sluitBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                                                              
            mainWin = MainWindow()
            mainWin.exec_()

    win = MyWindow(data_list, header)
    win.exec_()
    zoeken(m_email)