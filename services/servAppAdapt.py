import sys
import os
import pprint
import re

import Cookie 

mypath = os.path.dirname( os.path.realpath(__file__) )

sys.path.append( mypath + '/../model/dto' )
#print( os.path.dirname( os.path.realpath(__file__) ) + '/../model/dto' )

import appuser
from appuser import * 

import roleProps
from roleProps import *



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

class ServAppAdapt( object ):
	def __init__(self, env, start_response ):

                self.status = '200 OK'

                self.start_response = start_response
                self.env = env
                print('ENNNNNNNNNNNNNNNNVIIIIIIIIIIIRRRONNN')
		#pprint.pprint( self.env ) 

		self.resp_head = []	

		#self.resp_head.extend( tuple( [ 'Content-type', x ] ) for x in ['application/json'] ) 
		self.resp_head.append( tuple( [ 'Content-type', 'application/json' ] ) ) 

		#print( list( self.resp_head ) )  

		

		self.response_headers = [
			( 'Content-Type', 'application/json' ) #,
                        #( 'Content-Length', str( len( output + ',RAISER : ' + '______________________________________') ) )
                ]

		

	def adaptAppConf( self, rbc ):
		to_json = []

		rets =[] 
                print('ZZZZZZZZZZZZZZZZZZZZENNNNNNNNNNNNNNNNVIIIIIIIIIIIRRRONNN')
		print('{}'.format( rbc['rbac'][0].getPrior() ), rbc['rbac'][0].getRolename(), rbc['rbac'][0].getRoleUser(), rbc['rbac'][0].getPriorBehav() )		
		#rp = RoleProps('placeholderForAllowedFunc', '{}'.format( rbc['rbac'][0].getPrior() ), rbc['rbac'][0].getRolename(), rbc['rbac'][0].getRoleUser(), rbc['rbac'][0].getPriorBehav())
		
		print('___________________________________________________  {}'.format( self.env['QUERY_STRING'] ))				
		#print(dir(rp))
		#print(rp.getRoleId())

		
		self.qStr = {}
	
			
		if( re.match( '.*&.*', self.env['QUERY_STRING'] ) ):
			qList = self.env['QUERY_STRING'].split('&')
			
			for q in qList:
				self.qStr[ q.split('=')[0].strip() ] = q.split('=')[1].strip()
		
		elif( re.match( '.*=.*', self.env['QUERY_STRING'] ) ):
			
			self.qStr[ self.env['QUERY_STRING'].split('=')[0].strip() ] = self.env['QUERY_STRING'].split('=')[1].strip()
		
		else:	
			pass	
	
	
		print('END___________________________________________________  {}%'.format( self.env['QUERY_STRING'] ))				
		
		try:
			if( self.qStr['action'] == 'save' ):
				#rp = RoleProps('somefnc', '200', 'admin', 'test', 'equals:lower')

				#pprint.pprint( DaoDataMan({'foo':'bar'}, rp).listSearchRes( SearchDt('test%') ) )

				#pprint.pprint( DaoDataMan({'foo':'bar'}, rp).adaptApplic() )
				
				''' 
				IMPORTANT -- ALL APP-ADAPT-METHODS DON'T HAVE ANY ROLE-PRIORITY-CHECKS INTO THE SQL-QUERIES,
				JUST AN RBAC-CHECK BY ROUTING IT, CAUSE JUST ADMINS HAS THE PERSMISSION TO CHANGE THE AOO-BEHAVIOUR
				'''
				map( lambda x: DaoDataMan( rbc['dbh'], RoleProps( x.split('_')[0], 'prLevPlHld', self.qStr['selRole'], 'emailPlHld', x.split('_')[1] ) ).adaptApplic(), str( self.qStr['functionalities'] ).split('-') )
			

			elif( self.qStr['action'] == 'remove' ):	
				#raise Exception
				map( lambda x: DaoDataMan({'foo':'bar'}, RoleProps( x.split('_')[0], 'prLevPlHld', self.qStr['selRole'], 'emailPlHld', 'behavPlchldr' ) ).removeFuncFromRole(), str( self.qStr['functionalities'] ).split('-') )

				

		except Exception as e:
			print( dir( e ) )	

		finally:
			pass

		print('\n\n\n\nINTO APPADAPTCONF SERVICE\n\n\n\n\n')
		self.start_response( self.status, self.resp_head )
		self.output = simplejson.dumps( to_json ) 

		return self.output	
