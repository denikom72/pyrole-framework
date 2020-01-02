import sys
import unittest 
sys.path.append('/var/www/wsgi/model')
''' need to import mostly just the modul which have to be tested '''
import daoDataMan
from daoDataMan import *

from DBMan import * 
from decDB import *
from daoSess import *
from DaoAuth import *

sys.path.append('/var/www/wsgi/model/dto')

import appuser
from appuser import *

import roleProps
from roleProps import *

import person
from person import *

sys.path.append('/usr/local/lib/python2.7/dist-packages')

import mysql.connector
from django.db import connection
 
from mysql.connector import Error

DBData = {	'host' : 'localhost',
		'db' : 'comeandgo',
		'user' : 'root',
		'pw' : 't00rt00r'
}


persNm = 'pers1'
surname = 'surname1'
position = 'noPosition'
email = 'nox8LOLXyXXXgckmailo3@mail.com'
approle = 'manager'

''' User just for auth-unit-test '''
#usr = User('py5user@test.com', 'badpw123xy', '7')	

rp = RoleProps( 'DFUNC7', '200', approle, email, 'equals:lower' )


class TestDaoDataMan(unittest.TestCase):

	''' SETUP gonna be trigerred by every  '''
	def setUp(self):
		
		fakeVarForBP = 2 + 2 
		#rp = RoleProps( 'somefnc2', '200', approle, email, 'equals:lower' )
		pass	
		'''	
		self.dAuth = daoAuth()
		print(self.dAuth)
		
		
		lgdUsr = self.dAuth.startAuth(usr)
		
		self.dbSess = DaoSess( DBData ).checkSessID( usr )
			
		''' '''WRONG CREDENT CHECK''' '''
		self.assertFalse( DaoSess(DBData).checkSessID( User('wrongusr', 'wrongpw', 'wrongId') ) )
		'''
	def tearDown(self):
		'''  tearDown runs after every test, but we need the rollback after all tests are complete '''
		#self.dAuth.dbh.rollback()
		pass
	
	''' almost all ''' 

	def test_addUser(self):
		
		appuser = User( email, 'badpw123xy', '7' )
		print( dir( TestDaoDataMan.DBH ) )	
		''' 2 BENEFITS: a) no need to import some lybs to build test-queries b) can put rollback, instead of complicated delete-queries in the tearDown part and so on '''
		sql4ap = [ { 'query': 'SELECT email, passwordhash FROM users WHERE email LIKE %s', 'exec': [ email ] } ]
			
		ddm = DaoDataMan( TestDaoDataMan.DBH, rp ).addUser( appuser, testQuery = sql4ap, testQueryDto = lambda x: User( list(x)[0], list(x)[1] ).setPwdWithoutEncrypt( list(x)[1] ), test = True )
			
		ddmRes = []
			
		map( lambda x: ddmRes.append( [ u'{}'.format( x.getUsername() ), u'{}'.format( x.getPwd() ) ]  ), ddm )
		self.assertEqual( ddmRes, [ [ u'{}'.format( appuser.getUsername() ), u'{}'.format( appuser.getPwd() ) ] ] )
			
		''' trigger an error, wrong data-structur '''
		#self.assertEqual( ddmRes, [ u'{}'.format( appuser.getUsername() ), u'{}'.format( appuser.getPwd() ) ] )

	
		p = Person( 'somename', 'somesurname', 'noPosition', email )
		
		#raise Exception
		sql4ap = [ { 'query': 'SELECT * FROM person WHERE email LIKE %s', 'exec': [ email ] } ]
		ddm = DaoDataMan( TestDaoDataMan.DBH, rp ).addPerson( p, testQuery = sql4ap, testQueryDto = lambda x: Person( list(x)[0], list(x)[1], list(x)[2], list(x)[3] ), test = True )
			
		ddmRes = []
			
		map( lambda x: ddmRes.append( [ u'{}'.format( x.getName() ), u'{}'.format( x.getSurname() ), u'{}'.format( x.getPosition() ), u'{}'.format( x.getEmail() ) ]  ), ddm )
			
		self.assertEqual( ddmRes, [ [ u'{}'.format( p.getName() ), u'{}'.format( p.getSurname() ), u'{}'.format( p.getPosition() ), u'{}'.format( p.getEmail()) ] ] )
		''' trigger an error '''
		##self.assertEqual( ddmRes, [ u'{}'.format( p.getName() ), u'{}'.format( p.getSurname() ), u'{}'.format( p.getPosition() ), u'{}'.format( p.getEmail() ) ] )

	'''	
	def test_addPerson(self):
		
		p = Person( 'somename', 'somesurname', 'noPosition', email )
		
		#raise Exception
		sql4ap = [ { 'query': 'SELECT * FROM person WHERE email LIKE %s', 'exec': [ email ] } ]
		ddm = DaoDataMan( TestDaoDataMan.DBH, rp ).addPerson( p, testQuery = sql4ap, testQueryDto = lambda x: Person( list(x)[0], list(x)[1], list(x)[2], list(x)[3] ), test = True )
			
		ddmRes = []
			
		map( lambda x: ddmRes.append( [ u'{}'.format( x.getName() ), u'{}'.format( x.getSurname() ), u'{}'.format( x.getPosition() ), u'{}'.format( x.getEmail() ) ]  ), ddm )
			
		self.assertEqual( ddmRes, [ [ u'{}'.format( p.getName() ), u'{}'.format( p.getSurname() ), u'{}'.format( p.getPosition() ), u'{}'.format( p.getEmail()) ] ] )
		''' ''' trigger an error ''' '''
		self.assertEqual( ddmRes, [ u'{}'.format( p.getName() ), u'{}'.format( p.getSurname() ), u'{}'.format( p.getPosition() ), u'{}'.format( p.getEmail() ) ] )

	'''
	def test_addUser2Role(self):
		
		''' 2 BENEFITS: a) no need to import some lybs to build test-queries b) can put rollback, instead of complicated delete-queries in the tearDown part and so on '''
		sql4ap = [ { 'query': 'SELECT * FROM user_role WHERE user LIKE %s', 'exec': [ email ] } ]
		
		''' passing querystring-data to the roleprops-dto and also the role-name of the user who's logged in and roleId to which the user have to be add '''
		qStrRp = RoleProps( 'servAddUser', 0, rp.getRolename(), email  ).setRoleId(12)	
			
		ddm = DaoDataMan( TestDaoDataMan.DBH, rp ).addUser2Role( qStrRp, testQuery = sql4ap, testQueryDto = lambda x: rp.setRoleId( list(x)[0] ).setRoleUser( list(x)[1] ), test = True )
			
		ddmRes = []
		pprint.pprint(ddm)	
		
		map( lambda x: ddmRes.append( [ u'{}'.format( x.getRoleId() ), u'{}'.format( x.getRoleUser() ) ]  ), ddm )
		self.assertEqual( ddmRes, [ [ u'{}'.format( rp.getRoleId() ), u'{}'.format( rp.getRoleUser() ) ] ] )
		''' trigger an error, wrong data-structur '''
		#self.assertEqual( ddmRes, [ u'{}'.format( rp.getRoleId() ), u'{}'.format( rp.getRoleUser() ) ] )
		MOCKDBG = 'MOCKDBG'
	def test_selRoles(self):
	
		print('\n\n\nSEL ROLES\n\n\n')
		print( "{} - {} - {}".format( rp.getRolename(), str( rp.getRoleId() ), rp.getPrior() ) )
	
		ddm = DaoDataMan( TestDaoDataMan.DBH, rp ).selRoles(test = True)
		
		ddmRes = []
		
		map( lambda x: ddmRes.append( [ u'{}'.format( x.getRolename() ), u'{}'.format( x.getPrior() ), u'{}'.format( x.getRoleId() ) ]  ), ddm )
		print("\n\n\n\nSEL ROLES INTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\n\n\n\n")
		pprint.pprint(ddmRes)

		#print("\n\n\n\nINTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\n\n\n\n")
		
		#print( bln for bln in map( lambda x: '{:d}'.format( int( x[1] ) ) > '{:d}'.format( int( rp.getPrior() ) ), ddmRes ) )
		print( [ bln for bln in map( lambda x: int( x[1] ) > int( rp.getPrior() ), ddmRes ) ] )
		print( map( lambda x: '{:d} | {:d}'.format( int( x[1] ), int( rp.getPrior() ) ), ddmRes ) )
		
		''' it isn't allowed to list roles with higher priority as the role-priority of the user which trigger selRoles-Method  '''
		[ self.assertFalse( bln ) for bln in map( lambda x: int( x[1] )  >  int( rp.getPrior()  ), ddmRes ) ]
	
	
	''' add new methods, functionalities to a role '''	
	def test_adaptApplic(self):
		
		print("\n\n\n\n ADAPT APPLIC PART INTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO \n\n\n\n", rp.getRolename() )
		sql4ap = [ {     'query': ''' 	SELECT *, %s AS rlName FROM role_abil AS ra 
					
						WHERE ra.roleId = ( SELECT ro.id FROM roles AS ro WHERE ro.name LIKE %s ) ''',
                                
				 'exec': [ rp.getRolename(), rp.getRolename() ]
                } ]	
			
		
				
		#ddm = DaoDataMan( TestDaoDataMan.DBH, RoleProps( 'DFUNC5', '200', 'manager', 'emailPlHld', 'lower' ) ).adaptApplic()
		ddm = DaoDataMan( TestDaoDataMan.DBH, rp ).adaptApplic( testQuery = sql4ap, testQueryDto = lambda x: RoleProps( x[1], 'plch', x[3], 'plch', x[2] ).setRoleId( int( x[0] ) ), test = True)
		ddmRes = []
		map( lambda x: ddmRes.append( [ u'{}'.format( x.getRolename() ), u'{}'.format( x.getFunct() ), u'{}'.format( x.getPriorBehav() ) ] ), ddm )
		self.assertTrue( [ rp.getRolename(), rp.getFunct(), rp.getPriorBehav()  ] in ddmRes )	
	
	''' FIRST ADD FUNCS BY ROLE ABOVE, THEN SELECT CAN THROW SOME RESULTS  '''
	def test_selFuncsByRole(self):
		
		#rp2 = RoleProps( 'somefncXYZ', '12', approle, email, 'equals:lower' )
		
		ddm = DaoDataMan( TestDaoDataMan.DBH, rp ).selFuncsByRole( testQuery = [], test = True )
		ddmRes = []
		
		map( lambda x: ddmRes.append( [ u'{}'.format( x.getFunct() ), u'{}'.format( x.getPriorBehav() ) ] ), ddm )
		'''
		assrt = False
		
		for i in ddm:
			if 'somefnc2' == i.getFunct():
				assrt = True
		'''

		assrt = True if True in map( lambda x: rp.getFunct() in [ x.getFunct() ], ddm) else False
	
		self.assertTrue(assrt)
		
		#print( bln for bln in map( lambda x: '{:d}'.format( int( x[1] ) ) > '{:d}'.format( int( rp.getPrior() ) ), ddmRes ) )
		''' it isn't allowed to list roles with higher priority as the role-priority of the user which trigger selRoles-Method  '''
		#[ self.assertFalse( bln ) for bln in map( lambda x: '{:d}'.format( int( x[1] ) ) > '{:d}'.format( int( rp.getPrior() ) ), ddmRes ) ]

	def test_removeFuncFromRole( self ):
		
		print("\n\n\n\n ADAPT APPLIC PART INTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO \n\n\n\n", rp.getRolename() )
		sql4ap = [ {     'query': ''' 	SELECT *, %s AS rlName FROM role_abil AS ra 
					
						WHERE ra.roleId = ( SELECT ro.id FROM roles AS ro WHERE ro.name LIKE %s ) ''',
                                
				 'exec': [ rp.getRolename(), rp.getRolename() ]
                } ]	
			
		
				
		#ddm = DaoDataMan( TestDaoDataMan.DBH, RoleProps( 'DFUNC5', '200', 'manager', 'emailPlHld', 'lower' ) ).adaptApplic()
		
		#ddm = DaoDataMan( TestDaoDataMan.DBH, rp ).removeFuncFromRole()
		
		ddm = DaoDataMan( TestDaoDataMan.DBH, rp ).removeFuncFromRole( testQuery = sql4ap, testQueryDto = lambda x: RoleProps( x[1], 'plch', x[3], 'plch', x[2] ).setRoleId( int( x[0] ) ), test = True )
		ddmRes = []

		map( lambda x: ddmRes.append( [ u'{}'.format( x.getRolename() ), u'{}'.format( x.getFunct() ), u'{}'.format( x.getPriorBehav() ) ] ), ddm )
		bln = True
		bln = False if [ rp.getRolename(), rp.getFunct(), rp.getPriorBehav()  ] not in ddmRes else True
		self.assertFalse( bln )	
		
		
	



#if __name__ == '__main__':
#	unittest.main()

#	suite = unittest.TestLoader().loadTestsFromTestCase( TestDaoDataMan )
#	unittest.TextTestRunner(verbosity=2).run(suite)
