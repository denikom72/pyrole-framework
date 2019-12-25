import sys
import pprint

sys.path.append('/var/www/wsgi/model')

from DBMan import * 

sys.path.append('/var/www/wsgi/model/dto')
import appuser
from appuser import *


sys.path.append('/usr/local/lib/python2.7/dist-packages')

import mysql.connector
from django.db import connection
 
from mysql.connector import Error

class daoAuth( object ):
	
	def __init__(self):
		self.sth = None	
	
		DBData = {	'host' : 'localhost',
				'db' : 'comeandgo',
				'user' : 'root',
				'pw' : 't00rt00r'
		}
	
		dbm = DBMan( DBData )
		self.dbh = dbm.getDbh()
	
	
	def addAppuser( self, usr ):	
	
		print( dir( usr ) )
		SQL = [	
			{ 
				'query' : "INSERT INTO users ( email, passwordhash ) VALUES ( %s, %s )",
				'exec' : tuple( [ usr.getUsername(), usr.getPwd() ] )
			}
		]
		
		pprint.pprint( dir( self.dbh.cursor ) )
		pprint.pprint( SQL )			
		
		#raise Exception()	
		try:
			
			#print dir( mysql.connector )
			
			self.sth = self.dbh.cursor()
			map( lambda x : self.sth.execute( x['query'], x['exec'] ), SQL )
			
			#record = self.sth.fetchall()
			print('\n\n\n\nCHECK AUTOCOM IN DAOAUTH TRY PART \n\n\n\n')
			print(self.dbh.autocommit)	
			self.dbh.commit()

		except mysql.connector.Error as err:
			
			'''
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Wrong credentials : {}".format( err ) )
			else:
				print(err)
			'''
			print(err)
			self.dbh.rollback()
			
		else:
			#self.dbh.close()
			print('/////////////////////////////////////////////////////////////////////////////////////////7')
		
		finally:
			''' closing database connection. '''
			if( self.dbh.is_connected() ):
				pass
				#self.sth.close()
				#self.dbh.close()
				#print("connection is closed")
	

	def startAuth( self, usr ):	
		SQL = [	
			# DELETE OLD COOKIE
			{ 
				'query' : '''UPDATE users SET sid = '' WHERE email LIKE %s''',
				'exec' : [ usr.getUsername() ]
			},
						
			# SET NEW COOKIE IF CREDENTIALS ARE RIGHT
			{ 
				'query' : '''UPDATE users SET sid = %s WHERE email LIKE %s AND passwordhash LIKE %s''',
				'exec' : [ usr.getSid(), usr.getUsername(), usr.getPwd() ]
			},
					
				 	
			{ 
				#'query' : "SELECT ROW_COUNT();", 
				'query' : '''SELECT sid, email FROM users WHERE email = %s AND passwordhash LIKE %s''', 
				'exec' : [ usr.getUsername(), usr.getPwd() ]
			}
		]
	
		self.sth = self.dbh.cursor()
		map( lambda x : self.sth.execute( x['query'], x['exec'] ), SQL )
		
		#usr.setSid('')

		#print usr.getUsername()
		#raise Exception()	
		
		try:
			
			#pprint.pprint( dir( self.dbh.cursor ) )
			
			record = self.sth.fetchall()
			
			self.dbh.commit()

			if(record):
				pprint.pprint( record )
			
			usr.setUsername( record[0][1] )
			usr.setSid( record[0][0] )

		except mysql.connector.Error as err:
			
			'''
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Wrong credentials : {}".format( err ) )
			else:
				print(err)
			'''
			print(err)
			#usr.setSid( 'TEST' )
				
			self.dbh.rollback()
			'''
		else:
			usr.setSid('TEST2')
			print usr.getSid()
		#	self.dbh.close()
			'''
		finally:
			''' closing database connection. '''
			if( self.dbh.is_connected() ):
		
				self.sth.close()
				#self.dbh.close()
				#print("connection is closed")
			
			return[ usr ]

#daoAuth().startAuth(User('pyuser2qmail.com', '2bec84f900411e07c50a01315b57dc3b', '12344rr44'))
