#from pythonlangutil.overload import Overload, signature
import sys
import os
import re
import pprint
sys.path.append('/usr/local/lib/python2.7/dist-packages')

import django

from django import template   
from django.template.loader import get_template
from django.template import Template, Context

mypath = os.path.dirname( os.path.realpath(__file__) )
sys.path.append( mypath + '/../model' )

import daoDataMan 
from daoDataMan import *

sys.path.append( mypath + '/../model/dto' )
import http
from http import *

class AppMan( object ):
	def __init__(self, env, start_response, rbac ):
		
		self.status = '200 OK'
		
		self.start_response = start_response
		self.env = env
		self.qStr = {}		
		
		'''	
		print("ENVIR")
		#pprint.pprint( env )
		print(self.env['QUERY_STRING'])
		print("END-ENVIR")
		'''

		self.http = Http( self.env['QUERY_STRING'] )

		self.rbac = rbac
		self.response_headers = [
                        ( 'Content-type', 'text/html' ) #,
                        #( 'Content-Length', str( len( output + ',RAISER : ' + '______________________________________') ) )
	        ]

	def listFuncs( self ):
		#pass
		mypath = os.path.dirname( os.path.realpath(__file__) )

		mainCont = mypath + '/../mainCont.py'
		
		fncs = []
		
		''' with include try-catch, so don't need this or while(<>) like in perl '''
		with open( mainCont, 'rt' ) as fl:
			for l in fl:
				if re.match(".*?rbac\['func'\].*?", l):
					
					nl = l.split(' in ')[0].replace('\'', '')

					nl = re.sub( r'.*?if\( ', '', nl )

					fncs.append( nl.strip() )

		pprint.pprint(fncs)
		
		
		return fncs	
		
		#sys.path.append( mypath + '/../model/dto' )
		#print( os.path.dirname( os.path.realpath(__file__) ) + '/../model/dto' )
	
	def listRoles( self ):
		rbc = self.rbac
		dtoList = ['ff']
		dtoList = DaoDataMan( rbc['dbh'], RoleProps('placeholderForAllowedFunc', '{}'.format( rbc['rbac'][0].getPrior() ), rbc['rbac'][0].getRolename(), rbc['rbac'][0].getRoleUser(), rbc['rbac'][0].getPriorBehav() ) ).selRoles()
		print('DTOLIST : ')
		pprint.pprint( dtoList )
		print( dir( dtoList[0] ) )
		#print( dtoList[0].getPrior() + " : " +  dtoList[0].getRolename() )
		#print( str( dtoList[0].getPrior() ) + " : " +  str( dtoList[0].getRolename() ) )
		print( "{1} -- {0}".format( dtoList[0].getPrior(), dtoList[0].getRolename()) )
	
		#print('ROLELIST : ')	
		#pprint.pprint( map( lambda x: x.getRolename(), dtoList ) )
		return list( map( lambda x: x.getRolename(), dtoList ) )
	
	def listFuncsByRole( self ):
		rbc = self.rbac
		dtoList = []
		fList = []	
		
		self.qStr = self.http.getQStr()
		
		'''
		print('RBAC ATTRIBUTSi\n\n\n')
		print( dir( rbc['rbac'][0] ) )
		

		if( not self.qStr['selRole'] ):
			self.qStr['selRole'] = rbc['rbac'][0].getRolename()
		'''
		
		try:
			if( self.qStr['selRole'] == '' ):
					#self.qStr['selRole'] = rbc['rbac'][0].getRolename()
					pass

		#except Exception as err:
		except KeyError as err:
			'''
			print('EXCEPTION ART \n\n\n\n\n')
			print( type(err).__name__ )
			'''
			print( err )
			#self.qStr['selRole'] = rbc['rbac'][0].getRolename()
			self.qStr['selRole'] = ''
		
		finally:
			role = self.qStr['selRole']

	
		dtoList = DaoDataMan( rbc['dbh'], RoleProps('placeholderForAllowedFunc', '{}'.format( rbc['rbac'][0].getPrior() ), role, rbc['rbac'][0].getRoleUser(), rbc['rbac'][0].getPriorBehav() ) ).selFuncsByRole( test = False )
		
		print('\n\n\n\n\n\n\n\nFUNCBYROLE-DTOLIST : ')
		pprint.pprint( dtoList )
		try:
			raise IndexError #as test error
		except Exception as e:
			excepName = type(e).__name__ # returns the name of the exception
			print('EXCEPTIONTEST')
			print( excepName )
			print( e.__doc__ )
			print( e.message )
			print(dir(e))
			print('ERRORTESTEND\n\n\n')
		try:
			print( dir( dtoList[0] ) )
		except IndexError as err:
			print(err)
		finally:
			pass
		
		#print( dtoList[0].getPrior() + " : " +  dtoList[0].getRolename() )
		#print( str( dtoList[0].getPrior() ) + " : " +  str( dtoList[0].getRolename() ) )
		#print( "{1} -- {0}".format( dtoList[0].getPrior(), dtoList[0].getRolename()) )
	
		print('\n\n\n\n\nFUNCTLIST : ')	
		map( lambda x: fList.append( [ x.getFunct(), x.getPriorBehav() ] ), dtoList )
		pprint.pprint(fList)
		return fList 
	
	def tpl( self ):
		
		t = get_template('applicationMan.html')
		#t = get_template('tplFuncTest.html')
		self.start_response( self.status, self.response_headers )

		self.output = b'New Output APPMAN' 

		funcs1 = self.listFuncs()
		roles = self.listRoles()
		try:
			funcsByRole = self.listFuncsByRole()
		except Error as err:
			print( err )
			funcsByRole = []
		
		
		#pprint.pprint( roles )
		self.output = str( t.render( { 'funcs1' : funcs1, 'roles' : roles, 'funcsByRole' : funcsByRole, 'http' : self.qStr } ) )
		#self.output = str( t.render( { 'roles' : ['bla'] } ) )

		return self.output
