# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from informacion.models import Region,Mesa,Centro
from html import *
from bs4 import BeautifulSoup
from termcolor import colored
#from informacion.models import Region
import os.path
dir_ele="http://www.cne.gob.ve/resultado_presidencial_2012/"

def traeRegion(link):
    pagina=html()
    intentos=0
    while True:
        try:
            pagina.html_connect(link)
            intentos=intentos+1
            if pagina.status==200:
                pagina.html_read()
                soup = BeautifulSoup(pagina.html_showHTML())
                return soup.find(id="regionNavigationBar").find_all('a')
            else:
                print colored('Error: Servidor No devuelve datos intento %i' % intentos,'red')
        except Exception, e:
            print( colored(" Error de descargando pagina intento %i" % intentos,'red'))
        if intentos==10:
            intentos=0
            while True:
                si=raw_input('Hay Problemas conectando, intento de nuevo (S/N)')
                si=si.lower()
                if si in ["s","n"]:
                    break
            if si=='n':
                print (colored('error cargando datos desde la pagina','red'))
                raise

def traeMesa(link):
    pagina=html()
    intentos=0
    while True:
        try:      
            pagina.html_connect(link)
            intentos=intentos+1
            if pagina.status==200:
                pagina.html_read()
                return  BeautifulSoup(pagina.html_showHTML())
            else:
                 print colored('Error: Servidor No devuelve datos intento %i' % intentos,'red')
        except Exception, e:
            print( colored(" Error de descargando pagina intento %i" % intentos,'red'))
        if intentos==10:
            intentos=0
            while True:
                si=raw_input('Hay Problemas conectando, intento de nuevo (S/N)')
                si=si.lower()
                if si in ["s","n"]:
                    break
            if si=='n':
                print (colored('error cargando datos desde la pagina','red'))
                raise

    

    
def GrabaRegion(self,region):
    dir_ele="http://www.cne.gob.ve/resultado_presidencial_2012/"
    self.stdout.write(colored(" %s - (%s)- %s" % (region.getText(),os.path.basename(region.get('href'))[4:10], region.get('href').replace("../../",dir_ele)),'yellow'))
    r=Region()
    c=os.path.basename(region.get('href'))[4:10]
    r.codigo_estado=c[0:2]
    r.codigo_municipio=c[2:4]
    r.codigo_parroquia=c[4:6]
    r.nombre=region.getText().encode('utf-8')
    r.link=str(region.get('href').replace("../..",dir_ele))
    try:
        r.save()
        self.stdout.write("Grabado")
    except Exception, e:
        self.stdout.write("Region ya existe")


def GrabaCentro(self,centro):
    self.stdout.write(colored(" %s - (%s)- %s" % (centro.getText(),os.path.basename(centro.get('href'))[4:13], centro.get('href').replace("../../",dir_ele)),'yellow'))
    c=Centro()
    n=os.path.basename(centro.get('href'))[4:13]
    c.codigo_estado=n[0:2]
    c.codigo_municipio=n[2:4]
    c.codigo_parroquia=n[4:6]
    c.codigo_centro=n[6:9]
    c.nombre=centro.getText().encode('utf-8')
    c.link=str(centro.get('href').replace("../..",dir_ele))
    try:
        c.save()
        self.stdout.write("Grabado")
    except Exception, e:
        self.stdout.write("Centro ya existe")

def CodigoEstado(estado):   
    codigo=os.path.basename(estado.get('href'))[4:10]
    return int(codigo[0:2])

def CodigoMunicipio(municipio):   
    codigo=os.path.basename(municipio.get('href'))[4:10]
    return int(codigo[2:4])

def GrabaMesa(self,mesa):
    self.stdout.write(colored(" %s - (%s)- %s" % (mesa.getText(),os.path.basename(mesa.get('href'))[4:16], mesa.get('href').replace("../../",dir_ele)),'yellow'))
    m=Mesa()
    n=os.path.basename(mesa.get('href'))[4:16]

    m.codigo_estado=n[0:2]
    m.codigo_municipio=n[2:4]
    m.codigo_parroquia=n[4:6]
    m.codigo_centro=n[6:9]
    m.codigo_mesa=n[9:12]
    m.eleccion=1
    m.nombre=mesa.getText().encode('utf-8')
    m.link=str(mesa.get('href').replace("../..",dir_ele))
    #Buscando información de los votos en la mesa
    try:
        if Mesa.objects.get(codigo_estado=m.codigo_estado, codigo_municipio=m.codigo_municipio, codigo_parroquia=m.codigo_parroquia, codigo_centro=m.codigo_centro, codigo_mesa=m.codigo_mesa):
            print(colored("Mesa ya esta en la base de Datos",'blue'))
            return
    except Exception, e:
        print 'Grabando..' 
    

  
    soup = traeMesa(m.link)
    contadorOtros=0
    if soup.find(id="tablaResultados"):
        for r in soup.find(id="tablaResultados").find_all(class_='tbsubtotalrow'):
            t=r.findAll(class_="lightRowContent")
            nombre=str(t[1].text.replace("Adjudicado","").strip())
            votos=int(t[2].text.replace(".",""))
         
            if nombre=='HUGO CHAVEZ':
                print ("Oficialismo - (%i)" % votos  )
                m.ch=votos
            elif nombre == 'HENRIQUE CAPRILES RADONSKI':
                print ("Oposicion - (%i)" % votos  )
                m.op=votos
            else:
                contadorOtros=contadorOtros+votos
        print ('Otros - (%i)' % contadorOtros) 
        m.ot=contadorOtros
        
        c=0
        for f in soup.find(id="fichaTecnica").find_all(class_='tblightrow'):
            c=c+1
            l=f.findAll("td")          
            if c==1:
                votos=int(l[2].text.replace(".",""))
                print ("Electores - (%s)" % ( votos ))
                m.electores=votos
            elif c==7:
                votos=int(l[2].text)
                print ("Votos Nulos - (%s)" % (votos)  )
                m.nulos=votos
    try:
        m.save()
        self.stdout.write("Mesa Grabada")
    except Exception, e:
        self.stdout.write("Mesa ya existe")


class Command(BaseCommand)  :
    args = '<#estado>, <#municipio> comenzar a buscar desde el Estado y municipo'
    help = 'Carga Informacion desde el Cne a la Base de Datos'

    def handle(self, *args, **options):
        comenzarEstado=0
        comenzarMunicipo=0

        if len(args)> 0 :
            comenzarEstado=int(args[0])
        if len(args)>1 :
            comenzarMunicipo=int(args[1])

        estados=traeRegion(dir_ele+"r/1/reg_000000.html?")
        #Grabando Estados
        ce=0
        for estado in estados:
            ce=ce+1
            if comenzarEstado==0 or ce>=comenzarEstado:
                GrabaRegion(self,estado)
                municipios=traeRegion(str(estado.get('href').replace("../../",dir_ele)))
                cm=0
                for municipio in municipios:
                    cm=cm+1
                    if comenzarMunicipo==0 or cm>=comenzarMunicipo or comenzarEstado!=ce:
                        GrabaRegion(self,municipio)
                        
                        parroquias=traeRegion(str(municipio.get('href').replace("../../",dir_ele)))
                        for parroquia in parroquias:
                            GrabaRegion(self,parroquia)
                            centros=traeRegion(str(parroquia.get('href').replace("../../",dir_ele)))
                            for centro in centros:
                                GrabaCentro(self,centro)
                                mesas=traeRegion(str(centro.get('href').replace("../../",dir_ele)))
                                for mesa in mesas:
                                    GrabaMesa(self,mesa)
                    
                    else:
                        print("Saltado el Municipio %i" % CodigoMunicipio(municipio))
            else:
                print("Saltado el Estado %i" % CodigoEstado(estado))