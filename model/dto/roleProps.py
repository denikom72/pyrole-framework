''' dto for more role-tables '''
class RoleProps(object):

	def __init__( self, funct, priority, rolename, roleuser = '', priorBehav = '' ):
		self.setFunct( funct )
		self.setPrior( priority )
		self.setRolename( rolename )
		self.setRoleUser( roleuser )
		self.setPriorBehav( priorBehav )
		#self.setPriorBehav( roleId )


	def setRoleUser( self, email ):
		self.__RoleUser = email
		return self


	def getRoleUser( self ):
		return self.__RoleUser
	
	
	def setFunct( self, func ):
		self.__Funct = func


	def getFunct( self ):
		return self.__Funct
	

	def setPrior( self, prior ):
		self.__Prior = prior


	def getPrior( self ):
		return self.__Prior
	

	def setRolename( self, rolename ):
		self.__Rolename = rolename
		return self


	def getRolename( self ):
		return self.__Rolename
	

	def setPriorBehav( self, PriorBehav ):
		self.__PriorBehav = PriorBehav

	def getPriorBehav( self ):
				
		self.__PriorBehav = self.__PriorBehav.replace('equals:lower', ' <= ')
		self.__PriorBehav = self.__PriorBehav.replace('lower', ' < ')

		#for i in map

		return self.__PriorBehav

	def setRoleId( self, RoleId ):
		self.__RoleId = RoleId
		return self


	def getRoleId( self ):
		return self.__RoleId
	
	''' just an example '''
	def setBundle( self, rolename, PriorBehav ):
		self.setRolename( rolename )
		self.setPriorBehav( PriorBehav )
		
		#important to return anonyme instances as method-params, cause constructor-overloading isn't possible
		return self

#print str (User('foo', 'bar').getName() )
