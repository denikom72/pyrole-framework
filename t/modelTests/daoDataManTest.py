import unittest

import sys
import pprint

sys.path.append('/var/www/wsgi/model')

from DBMan import * 
from decDB import *
from daoSess import *
from DaoAuth import *
from daoDataMan import *

sys.path.append('/var/www/wsgi/model/dto')
import appuser
from appuser import *

import searchDt
from searchDt import *

import roleProps
from roleProps import *

import searchRes
from searchRes import *

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

usr = User('py4user@test.com', 'badpw123xy', '7')	

persNm = 'pers1'
surname = 'surname1'
position = 'noPosition'
email = 'nomailo248@mail.com'
approle = 'manager'

rp = RoleProps( 'somefnc', '200', approle, email, 'equals:lower' )

class TestDaoDataMan(unittest.TestCase):

	''' test_ underscore is convention '''
	def test_startAuth( self ):
		''' WRITE TESTCASES '''
	
		# SHOULD BE INSTANCED OUTSIDE, CAUSE IT GENERATES BY INSTANCIING A RANDOM-SID AND PASS THE VALUE TO THE SET-ID ..

		self.assertTrue( daoAuth().startAuth(usr) )
		
		self.assertTrue( DaoSess(DBData).checkSessID( usr ) )
		
		''' WRONG CREDENT '''
		self.assertFalse( DaoSess(DBData).checkSessID( User('wrongusr', 'wrongpw', 'wrongId') ) )

	def test_rbacProps( self ):
		
		''' TEST WITH WRONG CREDENTIALS ''' 
		self.assertFalse( DaoSess(DBData).rbacProps( User('wrongusr', 'wrongpw', 'wrongId') ) )
		
		''' TEST WITH RIGHT CREDENTIALS ''' 
		self.assertTrue( DaoSess(DBData).rbacProps( usr ) )
		
	def test_addUser( self ):
		
		''' RIGHT CREDENT '''
		
		''' DATA FOR DTO '''

		self.assertTrue( Person( persNm, surname, position, email) )
		
		self.assertTrue( RoleProps('somefnc', '200', approle, email, 'equals:lower') )
		#self.assertTrue( rp.setRoleId(2) )
		
		self.assertTrue( User(email, 'badpw123xy', '7') )
		
		#pprint.pprint( DaoDataMan({'foo':'bar'}, rp).listSearchRes( SearchDt('test%') ) )
			
		pers = Person( persNm, surname, position, email )
		
		rp.setRoleId(2)
		
		appuser = User( email, 'badpw123xy', '7' )
		
		''' ADDUSER TEST '''
		self.assertTrue( DaoDataMan( {'foo':'bar'}, rp ).addUser( appuser ) == [], 'some trouble by adding an user' )
		self.assertEquals( DaoDataMan( {'foo':'bar'}, rp ).addPerson( pers ), [], 'some trouble by adding data to the table  person' )
		self.assertTrue( DaoDataMan( {'foo':'bar'}, rp ).addUser2Role( rp.setRoleId( DaoDataMan( {'foo':'bar'}, rp ).roleIdByRlName( rp )[0].getRoleId() ) ) == [] )
		''' ADDUSERTEST END '''
		

	def test_adaptApplic( self ):
		
		#DaoDataMan( {'foo':'bar'}, RoleProps(  'serAddUser', 'placeholder', 'moonrole', 'placeholder', 'equals:lower' ) ).adaptApplic()
		pass
	def test_removeFuncFromRole( self ):
		DaoDataMan( {'foo':'bar'}, RoleProps(  'serAddUser', 'placeholder', 'moonrole', 'placeholder', 'equals:lower' ) ).removeFuncFromRole()
		#pass
		#print("MODELTEST-SELFUNCBYROLE\n\n\n\n\n\n")

	def test_selFuncsByRole( self ):
		DaoDataMan( {'foo':'bar'}, rp ).selFuncsByRole()
		#print( RoleProps( 'placeholder', 'list', 'list', 'list' ).getRolename() )
		pass
		print("END MODELTEST")


#DaoDataManTest().runTests()
#DaoSess(DBData).checkSessID( User('py4user@test.com', 'badpw123xy', '7') )

#if __name__ == '__main__':
	
	#unittest.main()

#	suite = unittest.TestLoader().loadTestsFromTestCase( TestDaoDataMan )
#	unittest.TextTestRunner(verbosity=2).run(suite)
