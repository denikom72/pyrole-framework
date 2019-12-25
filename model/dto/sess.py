import appuser
from appuser import *

class Sess(User):

	def __init__( self, username, Rbac, sid = ''):
		self.setUsername( username )
		self.setRbac( Rbac )
		self.setSid( sid )

	def setRbac( self, Rbac ):
		self.__Rbac = Rbac


	def getRbac( self ):
		return self.__Rbac
	
	''' just an example '''
	def setBundle( self, email, Rbac ):
		self.setUsername( email )
		self.setRbac( Rbac )
		
		#important to return anonyme instances as method-params, cause constructor-overloading isn't possible
		return self

#print str (User('foo', 'bar', '12133').getUsername() )
