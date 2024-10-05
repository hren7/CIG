# Client Invoice Generator

import os, os.path

import cherrypy

import formatclients
import formatgenerate
import formathistory
from formatinvoice import mainInvoice, SaveHistory


class CIG(object):
    @cherrypy.expose
    def index(self):
        return open("index.html")
    
    @cherrypy.expose
    def clients(self):
        formatclients
        return open("html/clients.html")
    
    @cherrypy.expose
    def generate(self):
        formatgenerate
        return open("html/generate.html")
    
    @cherrypy.expose
    def invoice(self, client, hrlyrate, hours, save='False'):
        mainInvoice(str(client), float(hours), float(hrlyrate))
        if save == 'True':
            SaveHistory(client, hrlyrate, hours)
        return open("html/invoice.html")
     
    @cherrypy.expose
    def history(self):
        formathistory
        return open("html/history.html")


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.quickstart(CIG(), '/', conf)