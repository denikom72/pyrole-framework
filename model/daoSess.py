import sys
import pprint

sys.path.append('/var/www/wsgi/model')

from DBMan import * 

sys.path.append('/var/www/wsgi/model/dto')
import appuser
from appuser import *

import roleProps
from roleProps import *

sys.path.append('/usr/local/lib/python2.7/dist-packages')

import mysql.connector
from django.db import connection
 
from mysql.connector import Error

class DaoSess( object ):
	
	def __init__(self, DBData):
		self.sth = None	
	
	
		dbm = DBMan( DBData )
		self.dbh = dbm.getDbh()
	
	
	def rbacProps( self, usr ):	
		
		SQL = [ { 
			'query' : '''
				SELECT 
					ra.functionality  AS func, 
					r.priority AS prior, 
					r.name AS role,
					%s AS usr, 
					ra.priorBehav AS priorBeh 
				
				FROM role_abil AS ra 
				
					LEFT JOIN 

				roles AS r ON ra.roleId = r.id 
		
					WHERE 

				ra.roleId = ( SELECT roleId FROM user_role AS ur WHERE ur.user LIKE %s );''',

			'exec' :  [ usr.getUsername(), usr.getUsername() ]
		} ]
	
		'''
			testSql2 = "
				SELECT 
					ra.functionality  AS func, 
					r.priority AS prior, 
					r.name AS role, 
					'foo@muu.com' AS usr 
				
				FROM 
					role_abil AS ra 

				LEFT JOIN 
				
					roles AS r 

				ON 

					ra.roleId = r.id 

				WHERE 

					ra.roleId = ( SELECT roleId FROM user_role AS ur WHERE ur.user LIKE 'user123@test.com' );"
		'''
		
		self.sth = self.dbh.cursor()
		
		map( lambda x : self.sth.execute( x['query'], x['exec'] ), SQL )
		
		record = [] 	
		
		dtoList = []
	
		try:
			'''
			record = self.sth.fetchall()

			# [ dtoList.append( RoleProps( x[0], x[1], x[2], x[3], x[4] ) ) for x in record ]

			for x in record :
				dtoList.append( RoleProps( x[0], x[1], x[2], x[3], x[4] ) )
			'''
			
			map( lambda x : dtoList.append( RoleProps( x[0], x[1], x[2], x[3], x[4] ) ), self.sth.fetchall() )
			
			self.dbh.commit()
	
			if(record):
				#pprint.pprint( b'record' )
				pass
			
			''' record is list of tuples '''

			#pprint.pprint( list( map( lambda x : [ list(x)[4].replace( 'lower', ' =================== ' ) or list(x)[4].replace('=', '_') ], record ) ) )
			#pprint.pprint( list( map( lambda x : [ x[4].replace( 'lower', ' =================== ' ) ], record ) ) )
			
			'''	
			for i in range( 0, len( record ) ) :
				#print(i)
				L = list( record[i] )
				L[4] = L[4].replace('lower', '<')
				L[4] = L[4].replace('equals:lower', '=<')
				record[i] = tuple( L )
			'''	

		
		except mysql.connector.Error as err:
			
			'''
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Wrong credentials : {}".format( err ) )
			else:
				print(err)
			'''
			print(err)
			self.dbh.rollback()
			record = []
		
		finally:
			''' closing database connection. '''
			if( self.dbh.is_connected() ):
		
				self.sth.close()
				#self.dbh.close()
				#print("connection is closed")
	
		#pprint.pprint( dtoList )
		
		return( dtoList ) 

	
	def checkSessID( self, usr ):	
		
		#print(usr.getUsername(), usr.getSid())
		
		SQL = [ { 
			'query' : 'SELECT email, sid FROM users WHERE email LIKE %s AND sid LIKE %s',

			'exec' :  [ usr.getUsername(), usr.getSid() ]
		} ]
	
		
		self.sth = self.dbh.cursor()
		
		map( lambda x : self.sth.execute( x['query'], x['exec'] ), SQL )
		
		record = [] 	
		
		dtoList = []
		
		'''	
		pprint.pprint(usr)
		print( usr.getUsername() )	
		#record = self.sth.fetchall()
		
		print('recordddddddddddddddddddddddddddddd')	
		if(record):
			pprint.pprint( record )
		print('ENDDDDD REC')
		'''

		try:
			
			map( lambda x : dtoList.append( usr.setBundle( x[0], x[1] ) ), self.sth.fetchall() ) 
			
			self.dbh.commit()

			#print("INTRO")
			

		except mysql.connector.Error as err:
			
			print(err)
			self.dbh.rollback()
			record = []
		
		finally:
			''' closing database connection. '''
			if( self.dbh.is_connected() ):
		
				self.sth.close()
				#self.dbh.close()
				#print("connection is closed")
	
				#pprint.pprint( dtoList )
		
				return( dtoList ) 

''' TESTS '''

DBData = {	'host' : 'localhost',
		'db' : 'comeandgo',
		'user' : 'root',
		'pw' : 't00rt00r'
}

''' TEST WITH WRONG CREDENTIALS ''' 
#DaoSess(DBData).checkSessID( User('py3user@test.com', 'f9857e0fc56612db6d961200cd0e39bf', 'd99e159d290d7eaf244bb9310acb6') )
#DaoSess().rbacProps( User('py3user@test.com', 'f9857e0fc56612db6d961200cd0e39bf', 'd99e159d290d7eaf244bb9310acb6') )

''' TEST WITH RIGHT CREDENTIALS ''' 
#DaoSess(DBData).checkSessID( User('py3user@test.com', 'f9857e0fc56612db6d961200cd0e39bf', 'dd99e159d290d7eaf244bb9310acb6') )
#DaoSess().rbacProps( User('py3user@test.com', 'f9857e0fc56612db6d961200cd0e39bf', 'dd99e159d290d7eaf244bb9310acb6') )
