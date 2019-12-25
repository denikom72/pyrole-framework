class SearchDt(object):

	def __init__( self, searchStr ):
		self.setSearchStr( searchStr )
		print('INSTAAANC2')
	
	
	def setSearchStr( self, searchStr ):
		self.__searchStr = searchStr


	def getSearchStr( self ):
		return self.__searchStr
	
	
	''' just an example '''
	'''
	def setBundle( self, email, PriorBehav ):
		self.setRolename( email )
		self.setPriorBehav( PriorBehav )
		
		#important to return anonyme instances as method-params, cause constructor-overloading isn't possible
		return self
	'''
#print str ( SearchDt('%aa%').getSearchStr() )
