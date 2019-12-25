#from pythonlangutil.overload import Overload, signature
import sys
import os
import pprint

sys.path.append('/usr/local/lib/python2.7/dist-packages')

import django

from django import template   
from django.template.loader import get_template
from django.template import Template, Context

mypath = os.path.dirname( os.path.realpath(__file__) )
sys.path.append( mypath + '/../model/dto' )

import roleProps
from roleProps import *


sys.path.append( mypath + '/../model' )

import daoDataMan 
from daoDataMan import *

class LogDone( object ):
	def __init__(self, env, start_response, rbac ):
		
		self.status = '200 OK'
		
		self.start_response = start_response
		self.env = env

		
		
		self.rbac = rbac
		
		print('((((((((((((((((((((((((((((((((((((((((')
		print( dir( rbac['rbac'][0] ))
		print(self.rbac)
		
		#pprint.pprint( self.env ) 

		self.response_headers = [
                        ( 'Content-type', 'text/html' ) #,
                        #( 'Content-Length', str( len( output + ',RAISER : ' + '______________________________________') ) )
	        ]

	def tpl( self ):
		
		roleInst = DaoDataMan( self.rbac['dbh'], RoleProps( 'funcplchldr', self.rbac['rbac'][0].getPrior(), 'roleplchldr', 'userplchldr', self.rbac['rbac'][0].getPriorBehav() ) ).selRoles()
		print('INTO TPLTPLTPLTPLTPLTPLTPL')
		pprint.pprint(roleInst)	
		
		roles = []
		for ins in roleInst:
			roles.append( [ ins.getRolename(), ins.getPrior() ] )

		myvars = { 
			'user' : self.rbac['user'].getUsername(),
			'sid' : self.rbac['user'].getSid(),
			#role : self.rbac[0],
			'rbac' : self.rbac['func'],
			'roles' : roles 
			#companies : comp, 
			#rfids : rfid 
		}	
	
		pprint.pprint( myvars)		
		t = get_template('loginDone.html')
		#self.output = str( t.render(c) )
			
		self.start_response( self.status, self.response_headers )
		self.output = str( t.render(myvars) )
		
		#self.output = b'New Output' 

		return self.output
