import sys
import pprint
from warnings import warn
#from abc import ABC, abstractmethod

sys.path.append('/var/www/wsgi/controller');
sys.path.append('/var/www/wsgi/services');

from contFact import *
from servFact import *

sys.path.append('/var/www/wsgi/model')
from DBMan import * 

sys.path.append('/var/www/wsgi/model/dto')
import daoSess
from daoSess import * 

import appuser
from appuser import *

class MainCont(object):
			
	def __init__(self):
		self.status = '200 OK'
		self.output = ''
		
		self.response_headers = [
                        ( 'Content-type', 'text/html' ) 
	        ]
	
	''' DECORATOR_WRAPPER '''
	@classmethod
	def funct( cls, env, funcSign, decorated_wrapped ):
		def wrppr( *args, **kwargs ):
			#print(dir(cls))
			
			rbac = cls.chkRbac(env)
			
			if( funcSign in rbac['func'] or 'all' in rbac['func'] ):
				decorated_wrapped( *args, **kwargs )
		return wrppr
	
	@classmethod
	def chkRbac( cls, env ) :
	
		pprint.pprint(env)
		print(env['HTTP_COOKIE'])
		
		DBData = {	'host' : 'localhost',
				'db' : 'comeandgo',
				'user' : 'root',
				'pw' : 't00rt00r'
		}

		''' TODO : INSTANCIING daoSess, delegate DBData, use chkSid resp. setChckSid checkSessID, ... '''	
		ckies = env['HTTP_COOKIE'].split(';')
		pprint.pprint( ckies )
		dsess = DaoSess(DBData)
		
		print( dir( dsess ) )
		#raise Exception('fffffffff')
	
		'''
		sessData = {	ckies[0].split('=')[0].strip() : ckies[0].split('=')[1].strip(),
				ckies[1].split('=')[0].strip() : ckies[1].split('=')[1].strip()
		}
		'''

		sessData = {}
		
		def fillDict( sessData, key, val ):
			try:
				sessData[key] = val
			except Exception as err: 
				print('FILLDICT-ERROR : ' + err)
				sessData['noKey'] = 'noVal'
		
		for v in ckies:
			try:
				if( v.strip() != '' ):
					print( v.split('=')[0].strip() + " ------ " + v.split('=')[1].strip() )
					sessData[ v.split('=')[0].strip() ] = v.split('=')[1].strip()
					pprint.pprint(sessData)
			except Exception as e:
				print('LOOP OR ASSIGNMENT EXCEPTION : ' + e)
				sessData['placeholder'] = 'placeholder'

		pprint.pprint(sessData)

		'''


		try:
			map( lambda x: fillDict( sessData, x.split('=')[0].strip(), x.split('=')[1].strip() ), ckies )
		except Exception as err:
			print('MAPPPPEXCEPTION : ' +  err)
		'''
		print('############################')
		''' REAL BAD TROUBLE CAUSE THE ORDER OF THE COOKIES IS NOT ALWAYS THE SAME '''
		''' usr = User( ckies[0].split('=')[1].strip(), 'nopw', ckies[1].split('=')[1].strip() ) '''

		usr = User( sessData['user'], 'placeholder', sessData['sid'] )
		
		funcList = []
		
		if( len( dsess.checkSessID( usr ) ) > 0 ):
			
			print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
			#print( [  dir(i)  for i in funcs ] )

			rbc = dsess.rbacProps( usr )
			map( lambda x : funcList.append(x.getFunct() ), rbc )
			pprint.pprint(funcList)	
			'''	
			if( 'doLogin' in funcList ):
				print('doLogin is allowed')
			'''
			
		return {
			'func': funcList,
			'user': usr,
			'rbac': rbc,
			'dbh': dsess.dbh
		}

	''' TODO : RE-CODE METHOD AS DECORATOR '''

	@classmethod
	#@abstractmethod
	def loginform( cls, env, start_response ):
		#return TestContr( env, start_response ).tpl() 	
		return ContFact.loginForm( env, start_response ) 	
	
	@classmethod
	#@abstractmethod
	def servLogin( cls, env, start_response ):
		
		return ServFact.serviceLogin( env, start_response ) 	
	
	@classmethod
	#@abstractmethod
	def servSearch( cls, env, start_response ):
		
		#cls.func( env, 'doLogin', cls.sendHead )	
		rbac = cls.chkRbac(env)
		
		#print('\n\n\n\n\nCHKRBAC FUNC ABOVE\n\n\n\n')
		#pprint.pprint(rbac)
		#raise Exception()	
		
		if( 'servSearch' in rbac['func'] or 'all' in rbac['func'] ):
			#print(ServFact.serviceSearch( env, start_response ))
			return ServFact.serviceSearch( env, start_response, rbac ) 	
	
	@classmethod
	#@abstractmethod
	def servRoleMan( cls, env, start_response ):
		
		#cls.func( env, 'doLogin', cls.sendHead )	
		rbac = cls.chkRbac(env)
		
		print('CHKRBAC FUNC ABOVE')
		#pprint.pprint(rbac)
		#raise Exception()	
		if( 'servRoleMan' in rbac['func'] or 'all' in rbac['func'] ):
			#print(ServFact.serviceSearch( env, start_response ))
			return ServFact.serviceRoleMan( env, start_response, rbac ) 	
	
	@classmethod
	#@abstractmethod
	def servAddUser( cls, env, start_response ):
		
		#cls.func( env, 'doLogin', cls.sendHead )	
		rbac = cls.chkRbac(env)
		
		print('CHKRBAC FUNC ABOVE')
		#pprint.pprint(rbac)
		#raise Exception()	
		if( 'servAddUser' in rbac['func'] or 'all' in rbac['func'] ):
			#print(ServFact.serviceSearch( env, start_response ))
			return ServFact.serviceAddUser( env, start_response, rbac ) 	
	
	@classmethod
	#@abstractmethod
	def servAppAdapt( cls, env, start_response ):
		
		#cls.func( env, 'doLogin', cls.sendHead )	
		rbac = cls.chkRbac(env)
		
		print('CHKRBAC FUNC ABOVE')
		#pprint.pprint(rbac)
		#raise Exception()	
		if( 'all' in rbac['func'] ):
			#print(ServFact.serviceSearch( env, start_response ))
			return ServFact.serviceAppAdapt( env, start_response, rbac ) 	
	
	@classmethod
	def appMan( cls, env, start_response ):
		print('CHKRBAC FUNC ABOVE')
		#cls.func( env, 'doLogin', cls.sendHead )	
		rbac = cls.chkRbac(env)
		
		#pprint.pprint(rbac)
		#raise Exception()	
		if( 'all' in rbac['func'] ):
			#print('CONDITION TRUE')
			return ContFact.appMan( env, start_response, cls )	
	
	@classmethod
	def loginDone( cls, env, start_response ):
		print('CHKRBAC FUNC ABOVE')
		#cls.func( env, 'doLogin', cls.sendHead )	
		rbac = cls.chkRbac(env)
		
		#pprint.pprint(rbac)
		
		#raise Exception()	
		if( 'doLogin' in rbac['func'] or 'all' in rbac['func'] ):
			#print('CONDITION TRUE')
			return ContFact.loginDone( env, start_response, cls )	

		#return ContFact.loginDone( env, start_response, cls )	
