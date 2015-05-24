#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

"""
Make Html a list and store
"""

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.Content = ""
        self.Html = []
        self.Activity = {}

        self.inTitle = False
        self.inType = False
        self.inPrice = False
        self.inDate = False
        self.inEndDate = False
        self.inHour = False
        self.inDuration = False
        self.inUrl = False

    def startElement (self, name, attrs):
        if name == 'contenido':
            self.inItem = True
        elif self.inItem:
            if name == 'atributo':
                self.inContent = True
                nombre = attrs.getValue(u'nombre')

                if nombre == 'TITULO':
                    self.inTitle = True
                elif nombre == 'TIPO':
                    self.inType = True
                elif nombre == 'PRECIO':
                    self.inPrice = True
                elif nombre == 'FECHA-EVENTO':
                    self.inDate = True
                elif nombre == 'FECHA-FIN-EVENTO':
                    self.inEndDate = True
                elif nombre == 'HORA-EVENTO':
                    self.inHour = True
                elif nombre == 'EVENTO-LARGA-DURACION':
                    self.inDuration = True
                elif nombre == 'CONTENT-URL':
                    self.inUrl = True
            
    def endElement (self, name):
        if name == 'contenido':
            self.inItem = False
        elif self.inItem:
            if name == 'atributo':
                if self.inTitle:
                    self.Activity['title'] = self.Content
                    self.inTitle = False
                elif self.inPrice:
                    self.Activity['precio'] = self.Content
                    self.inPrice = False
                elif self.inDate:
                    self.Activity['fecha'] = self.Content
                    self.inDate = False
                elif self.inEndDate:
                    self.Activity['final'] = self.Content
                    self.inEndDate = False
                elif self.inHour:
                    self.Activity['hora'] = self.Content
                    self.inHour = False
                elif self.inDuration:
                    self.Activity['duracion'] = self.Content
                    self.inDuration = False  
                elif self.inUrl:
                    self.Activity['url'] = self.Content
                    self.inUrl = False  
                elif self.inType:
                    self.Activity['tipo'] = self.Content
                    self.inType = False
                    self.Html.append(self.Activity)
                    self.Activity = {}
                
                # To avoid Unicode trouble
                self.inContent = False
                    
                self.Content = ""

    def characters (self, chars):
        if self.inContent:
            self.Content = self.Content + chars
            
# --- Main prog
def getNews():  
    # Load parser and driver

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

    # Ready, set, go!
    theParser.parse("http://datos.madrid.es/portal/site/egob/" +
                    "menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/" +
                    "?vgnextoid=00149033f2201410VgnVCM100000171f5" + 
                    "a0aRCRD&format=xml&file=0&filename=206974-0-" +
                    "agenda-eventos-culturales-100&mgmtid=6c0b6d01" + 
                    "df986410VgnVCM2000000c205a0aRCRD")
    return theHandler.Html