class Person(object):

	def __init__( self, name, surname, position, email ):
		self.setName(name)
		self.setSurname(surname)
		self.setPosition( position )
		self.setEmail( email )	

	def setName( self, name ):
		self.__name = name

	def getName( self ):
		return self.__name
	
	def setSurname( self, surname ):
		self.__surname = surname

	def getSurname( self ):
		return self.__surname
	
	def setEmail( self, email ):
		self.__email = email

	def getEmail( self ):
		return self.__email
	
	def setPosition( self, position ):
		self.__position = position

	def getPosition( self ):
		return self.__position

''' TEST '''
#print str( Person( 'foo', 'bar', 'POSITION', 'dfdfd@kk.co' ).getPosition() )
