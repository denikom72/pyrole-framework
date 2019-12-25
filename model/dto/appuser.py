import sys

sys.path.append('/usr/local/lib/python2.7/dist-packages')

import md5
import random
from random import *

class User(object):

	def __init__( self, username, pwd, sid = '' ):
		self.__salt = '12dF-09'	
		
		self.setUsername( username )
		self.setPwd( pwd )
		self.setSid( sid )
		
		

	def setUsername( self, email ):
		self.__username = email


	def getUsername( self ):
		return self.__username
	

	def setPwd( self, pwd ):
			self.__pwd = md5.new( self.getUsername() + pwd + self.__salt ).hexdigest()

	''' JUST FOR UNIT-TESTING PURPOSE, FOR EXAMPLE WHEN YOU SET RESSET-VALUES FROM DATABASE FOR COMPARING IT, THEY SHOULDN'T BY ENCRYPTED AGAIN '''
	def setPwdWithoutEncrypt( self, pwd, crypted = True ):
		
		self.__pwd = pwd
		return self

	def getPwd( self ):
		return self.__pwd


	''' If sidNr just one or two characters, generate new sid, if it's a longer string, then there is already a generated sid, so just pass it to the private var '''
	def setSid( self, sidNr ):
		#chr( int('72') )
		self.__sid = sidNr
		if( len( str( sidNr ) ) < 2 ):
			self.__sid = md5.new( ''.join( list( map( lambda x : chr( int( "{}{}".format( str(sidNr), x )  ) ), str( random() ).replace( '.', '' ) ) ) ) ).hexdigest()
		#self.__sid =  random() 
		print('\n\n\n\nSID: ' + str( self.__sid ))

	def getSid( self ):
		return self.__sid
	
	''' just an example '''
	def setBundle( self, email, sid ):
		self.setUsername( email )
		self.setSid( sid )
		
		#important to return anonyme instances as method-params, cause constructor-overloading isn't possible
		return self

#print str (User('foo', 'bar').getSid() )
