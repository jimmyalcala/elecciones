from html import *
from bs4 import BeautifulSoup
#from informacion.models import Region
import os.path
pagina=html()
#http://www.cne.gob.ve/resultado_presidencial_2012/lvg/43/reg_220103007011.html
dir_ele="http://www.cne.gob.ve/resultado_presidencial_2012/"
pagina.html_connect(dir_ele+"lvg/43/reg_220103007011.html")
if pagina.status==200:
    pagina.html_read()
    soup = BeautifulSoup(pagina.html_showHTML())
    contadorOtros=0
    if soup.find(id="tablaResultados"):
        for r in soup.find(id="tablaResultados").find_all(class_='tbsubtotalrow'):
            t=r.findAll(class_="lightRowContent")
            nombre=str(t[1].text.replace("Adjudicado","").strip())
            votos=int(t[2].text)
         
            if nombre=='HUGO CHAVEZ':
                print ("Oficialismo - (%i)" % votos  )
            elif nombre == 'HENRIQUE CAPRILES RADONSKI':
                print ("Oposicion - (%i)" % votos  )
            else:
                contadorOtros=contadorOtros+votos
        print ('Otros - (%i)' % contadorOtros) 
            
        c=0
        for f in soup.find(id="fichaTecnica").find_all(class_='tblightrow'):
            c=c+1
            l=f.findAll("td")
            if c==1:
                print ("Electores - (%s)" % (l[2].text)  )
            elif c==7:
                print ("Votos Nulos - (%s)" % (l[2].text)  )

#pagina.html_close()
#b=Region()
