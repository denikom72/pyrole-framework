#from pythonlangutil.overload import Overload, signature
import sys
import os
import pprint
sys.path.append('/usr/local/lib/python2.7/dist-packages')

from django.conf import settings

''' SET TPL SETTINGS '''

#print ( os.path.dirname( os.path.realpath(__file__) ) + '/../view/' )
settings.configure(TEMPLATES=[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.dirname( os.path.realpath(__file__) ) + '/../view'], # if you want the templates from a file
        'APP_DIRS': False, # we have no apps
    },
])

import django
django.setup()


''' BIND CONTROLLERS '''

sys.path.append('/var/www/wsgi/controller')

import logForm 
from logForm import *

import logDone
from logDone import *

import appMan
from appMan import *
''' '''

class ContFact( object ):
	@classmethod
	def loginForm( cls, env, start_resp ):
		return LogForm( env, start_resp ).tpl()	

	@classmethod
	def loginDone( cls, env, start_resp, superCls ):
		
		#return LogForm( env, start_resp ).tpl()	
		print('----------------LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL')	
#		print(dir(env))
#		print(dir( superCls ) )
		pprint.pprint( superCls.chkRbac(env) ) 
		print('++++++++++++++++++++++LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL')	
#		#raise Exception('finish')
#		
		return LogDone( env, start_resp, superCls.chkRbac(env) ).tpl()	
	
	@classmethod
	def appMan( cls, env, start_resp, superCls ):
		return AppMan( env, start_resp, superCls.chkRbac(env) ).tpl()	

