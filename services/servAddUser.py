import sys
import os
import pprint

import Cookie 

mypath = os.path.dirname( os.path.realpath(__file__) )

sys.path.append( mypath + '/../model/dto' )
#print( os.path.dirname( os.path.realpath(__file__) ) + '/../model/dto' )

import appuser
from appuser import * 

import roleProps
from roleProps import *

import http
from http import *

#srchDt = SearchDt('dddd')
#print( srchDt.getSearchStr() )
#print('++++++++#####################################################')

sys.path.append( mypath + '/../model' )

import daoDataMan 
from daoDataMan import *

sys.path.append('/usr/local/lib/python2.7/dist-packages')

import random
from random import *

import md5
import json as simplejson

from django.http import HttpResponse

# IMPORT ABOVE WASN'T WORK, SOMETHING WAS OVERWRITED
import searchDt
from searchDt import *

class ServAddUser( object ):
	def __init__(self, env, start_response, rbc ):

                self.status = '200 OK'

                self.start_response = start_response
                self.env = env
                self.__rbc = rbc

		self.http = Http( self.env['QUERY_STRING'] )
		
		print('ENNNNNNNNNNNNNNNNVIIIIIIIIIIIRRRONNN')
		pprint.pprint( self.http.getQStr() ) 

		self.resp_head = []	

		#self.resp_head.extend( tuple( [ 'Content-type', x ] ) for x in ['application/json'] ) 
		self.resp_head.append( tuple( [ 'Content-type', 'application/json' ] ) ) 

		#print( list( self.resp_head ) )  

		

		self.response_headers = [
			( 'Content-Type', 'application/json' ) #,
                        #( 'Content-Length', str( len( output + ',RAISER : ' + '______________________________________') ) )
                ]

		




	def run( self ):
		to_json = []

		rets =[] 
		rbc = self.__rbc
		qStr = self.http.getQStr()

		print('{}'.format( rbc['rbac'][0].getPrior() ), rbc['rbac'][0].getRolename(), rbc['rbac'][0].getRoleUser(), rbc['rbac'][0].getPriorBehav() )		
		#raise Exception ('jjjjjjjjjjjjjjjjj')
		rp = RoleProps('placeholderForAllowedFunc', '{}'.format( rbc['rbac'][0].getPrior() ), rbc['rbac'][0].getRolename(), rbc['rbac'][0].getRoleUser(), rbc['rbac'][0].getPriorBehav() )
		
		print('___________________________________________________  {}'.format( self.env['QUERY_STRING'] ))				
		
		print(dir(rp))
		#print(rp.getRoleId())
		print('___________________________________________________  {}%'.format( self.env['QUERY_STRING'] ))				
		
		''' important to remember roleprops filled with rbc-data are delegated to the DaoDataMan-Constructor, not the http-data '''
		dataMan = DaoDataMan( rbc['dbh'], rp )

	
		''' important - here have to pass the http-qStr-data ''' 
		pers = Person( qStr['name'], qStr['surname'], qStr['position'], qStr['email'] )
		
		qStrRp = RoleProps( 'somefnc', '0', qStr['selRole'], qStr['email'] )
		
		appuser = User( qStr['email'], qStr['password'] )

		''' WORKAROUND CAUSE PRINT NOT POSSIBLE IN LAMBDA, RESP. MAP/LAMBDA-CONSTRUCT AND METHODS ARE NOT PASSEABLE AS PARAMS TO FOR-LOOP .... '''	
		for i in list( map( lambda x: x, dataMan.selRoles() ) ):
			#print( dir(i) )
			print( i.getRoleId() )

		#map( lambda x: qStrRp.setRoleId( str( x.getRoleId() ) ) if x.getRolename() == qStr['selRole'] else True, dataMan.selRoles() )
		qStrRp.setRoleId( dataMan.roleIdByRlName( qStrRp ) )
		print( '\n\n\n\n\n\n ROLEID --------> : ' + str( qStrRp.getRoleId() ) )
		
		dataMan.addUser( appuser )
		dataMan.addPerson( pers )
	
		dataMan.addUser2Role( qStrRp )
			
		print('\n\n\n\nINTO FAKE :SEARCH SERVICE\n\n\n\n\n')
		
		self.start_response( self.status, self.resp_head )
		self.output = simplejson.dumps( to_json ) 
		return self.output	
