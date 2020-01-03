import os, sys
from datetime import date
from PyQt5.QtWidgets import QApplication
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, create_engine,\
    insert, select, update, func

# set lock voor maximaal 1 sessie per PC
    
home = os.path.expanduser("~")
if os.path.isfile(str(home)+'/.pandora_lock'):
    sys.exit()
else:
    open(str(home)+'/.pandora_lock', 'w')
    
# volgende regels tbv jaarverbruik artikelen even/oneven jaar per jaar
# en berekenen van voorraadwaarde magazijnen t.b.v. grafieken per maand

metadata = MetaData()
artikelen = Table('artikelen', metadata,
    Column('artikelID', Integer(), primary_key=True),
    Column('artikelprijs', Float),
    Column('art_voorraad', Float),
    Column('mutatiedatum', String),
    Column('jaarverbruik_1', Float),
    Column('jaarverbruik_2', Float))
params = Table('params', metadata,
    Column('paramID', Integer, primary_key=True),
    Column('tarief', Float))
magazijnvoorraad = Table('magazijnvoorraad', metadata,
    Column('jaarmaand', String, primary_key=True),
    Column('totaal', Float),
    Column('courant', Float),                     
    Column('incourant', Float))
          
engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
con = engine.connect()
selpar = select([params]).where(params.c.paramID == 99)
rppar = con.execute(selpar).first()

mjaar = int(str(date.today())[0:4])
if mjaar%2 == 1 and int(rppar[1]) == 0:
    updpar = update(params).where(params.c.paramID == 99).values(tarief = 1)
    con.execute(updpar)
    updart = update(artikelen).values(jaarverbruik_2 = 0)
    con.execute(updart)
elif mjaar%2 == 0 and int(rppar[1]) == 1:
    updpar = update(params).where(params.c.paramID == 99).values(tarief = 0)
    con.execute(updpar)
    updart = update(artikelen).values(jaarverbruik_1 = 0)
    con.execute(updart)
    
mhjrmnd = str(date.today())[0:7]
mvjrmnd = int(str(int(str(date.today())[0:4])-1)+str(date.today())[5:7])
mdbjrmnd = (con.execute(select([func.max(magazijnvoorraad.c.jaarmaand, type_=Integer)\
                                   .label('mdbjrmnd')])).scalar())
if mhjrmnd != mdbjrmnd:
    insdb = insert(magazijnvoorraad).values(jaarmaand = mhjrmnd)
    con.execute(insdb)
    selart = select([artikelen])
    rpart = con.execute(selart)
    mtotaal = 0
    mcourant = 0
    mincourant = 0
    for row in rpart:
        mtotaal = mtotaal + row[1]*row[2]
        if mvjrmnd < int(str(row[3][0:4])+str(row[3])[5:7]):
            mcourant = mcourant + row[1]*row[2]
        else:
            mincourant = mincourant + row[1]*row[2]
    updmvrd = update(magazijnvoorraad).where(magazijnvoorraad.c.jaarmaand == mhjrmnd)\
          .values(totaal = int(mtotaal), courant = int(mcourant), incourant = int(mincourant))
    con.execute(updmvrd)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    from login import inlog
    inlog()
    app.exec_()
