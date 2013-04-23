from html import *
from bs4 import BeautifulSoup
#from informacion.models import Region
import os.path
pagina=html()
dir_ele="http://www.cne.gob.ve/resultado_presidencial_2012/"
#http://www.cne.gob.ve/resultado_presidencial_2012/r/2/reg_200701.html
pagina.html_connect(dir_ele+"r/2/reg_200701.html")
if pagina.status==200:
    pagina.html_read()
    soup = BeautifulSoup(pagina.html_showHTML())
    # r=soup.find(id="regionNavigationBar")
    for estado in soup.find(id="regionNavigationBar").find_all('a'):
    	print (" %s - (%s)- %s" % (estado.getText(),os.path.basename(estado.get('href'))[4:10], estado.get('href').replace("../..",dir_ele)))

    

#pagina.html_close()
#b=Region()
