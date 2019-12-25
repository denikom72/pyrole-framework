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

class ServSearch( object ):
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

		




	def jsnResp( self, rbc ):
		to_json = []
		rets =[] 
		print('{}'.format( rbc['rbac'][0].getPrior() ), rbc['rbac'][0].getRolename(), rbc['rbac'][0].getRoleUser(), rbc['rbac'][0].getPriorBehav() )		
		#raise Exception ('jjjjjjjjjjjjjjjjj')
		rp = RoleProps('placeholderForAllowedFunc', '{}'.format( rbc['rbac'][0].getPrior() ), rbc['rbac'][0].getRolename(), rbc['rbac'][0].getRoleUser(), rbc['rbac'][0].getPriorBehav())
		
		print('___________________________________________________  {}'.format( self.env['QUERY_STRING'] ))				
		
		print(dir(rp))
		#print(rp.getRoleId())
		print('___________________________________________________  {}%'.format( self.env['QUERY_STRING'] ))				

			
		#print('++++++++#####################################################')
		#srchDt = SearchDt('tes%')
		#print( srchDt.getSearchStr() )
	
	
		dtoList = DaoDataMan( rbc['dbh'], rp).listSearchRes( SearchDt( '{}%'.format( self.env['QUERY_STRING'] ) ) )
		#dtoList = DaoDataMan( {'foo':'bar'}, rp ).listSearchRes( SearchDt( 'test%' ) )
		
			
		print('\n\n\n\nINTO SEARCH SERVICE\n\n\n\n\n')
		#print( dir( rbc['rbac'][0] ) )
		#pprint.pprint( rbc['rbac'] )
		print( dir( dtoList[0] ) )
		print( len( dtoList ) )
		
		map( lambda x: to_json.append( { 'name' : x.getName(), 'surname' : x.getSurname(), 'email' : x.getRoleUser(), 'rolename' : x.getPosition(), 'role' : x.getRolename() } ), dtoList )	
		
		print('\n\nMMMMMMMMMMMMMMMMMMM\n\n')
		

		#print( dir( user ) )
		#print HttpResponse( simplejson.dumps(to_json), content_type='application/json' )
		#return HttpResponse( simplejson.dumps(to_json), content_type='application/json' )
		
		#self.start_response( self.status, self.response_headers )
		self.start_response( self.status, self.resp_head )
			
		#self.output = simplejson.dumps( [ { 'rets' : rets } ] ) 
		self.output = simplejson.dumps( to_json ) 
		#self.output = simplejson.dumps( rets ) 

		return self.output	
