import jinja2 as jj2
#from snakelegs.connection import connect
import sys
import web
import os

TEMPLATE_PATH = os.getcwd()+'/templates/'
STATIC_PATH = os.getcwd()+'/static/'
STATIC_URL = '/static/'

ENVIRON = jj2.Environment(loader=jj2.FileSystemLoader(TEMPLATE_PATH),
							autoescape=True)



