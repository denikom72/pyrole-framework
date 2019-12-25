import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages');

import mysql.connector
 

class DBMan(object):
	
	def __init__( self, dbProp ):
		
		#raise Exception (dbProp)
		self.setDbProps( dbProp )
		self.openDB()
		

	def setDbProps( self, dbData ):
		#TODO: PlausiCheck
		self.__dbProp = dbData

	
	def getDbProps( self ):
		return self.__dbProp

	
	def setDbh( self, dbh ):
		#TODO: PlausiCheck
		self.__dbh = dbh

	
	def getDbh( self ):
		return self.__dbh


	def openDB( self ):
	
		DBData = self.getDbProps();
		#raise Exception ( DBData )	
		#print Dumper $DBDATA;#die();
		
		try:
			conn = mysql.connector.connect(	host = DBData['host'],
							database = DBData['db'],
							user = DBData['user'],
							password = DBData['pw'] )
			conn.autocommit = False
			#print( conn.autocommit )
			#conn.autocommit = True
		
			self.setDbh( conn )
			print('connected')
		except mysql.connector.Error as e:
			print ( " DB ERROR : " + e )
		
		'''	
		print dir( mysql.connector )
	
		pprint.pprint( dir( conn ) )
		self.setDbh( conn )
		'''
		#unnecessary, cause accessor delivery dbh-instance 
		#return dbh;
	 

