import roleProps
from roleProps import *

class SearchRes(RoleProps):

	def __init__( self, name, surname, position, email, rolename, compId, priority ):
		self.setName(name)
		self.setSurname(surname)
		self.setPosition( position )
	
		self.setRoleUser( email )
		self.setRolename( rolename )
		self.setCompId( compId )
		self.setPrior( priority )

		print('INSTANCE333333333333')	
	def setName( self, name ):
		self.__name = name


	def getName( self ):
		return self.__name
	
	def setSurname( self, surname ):
		self.__surname = surname

	def getSurname( self ):
		return self.__surname
	
	def setPosition( self, position ):
		self.__position = position

	def getPosition( self ):
		return self.__position
	
	
	def setCompId( self, compId ):
		self.__compId = compId

	def getCompId( self ):
		return self.__compId

''' TEST '''
#print str( SearchRes( 'foo', 'bar', 'POSITION', 'dfdfd', 'dfdfd', 'dfdfdd', 'dfdfdf' ).getPosition() )
