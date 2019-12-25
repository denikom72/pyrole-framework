import unittest
 
from test_daoDataMan import *
 
sys.path.append('/var/www/wsgi/model')
from DBMan import * 

import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages');

import mysql.connector


from django.db import connection
 
from mysql.connector import Error

'''

import unittest

class MyTest(unittest.TestCase):

    def __init__(self, testName, extraArg):
        super(MyTest, self).__init__(testName)  # calling the super class init varies for different python versions.  This works for 2.7
        self.myExtraArg = extraArg

    def test_something(self):
        print(self.myExtraArg)

# call your test
suite = unittest.TestSuite()
suite.addTest(MyTest('test_something', extraArg))
unittest.TextTestRunner(verbosity=2).run(suite)

So the doctors here that are saying "You say that hurts? Then don't do that!" are probably right. But if you really want to, here's one way of passing arguments to a unittest test:

import sys
import unittest

class MyTest(unittest.TestCase):
    USERNAME = "jemima"
    PASSWORD = "password"

    def test_logins_or_something(self):
        print('username : {}'.format(self.USERNAME))
        print('password : {}'.format(self.PASSWORD))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        MyTest.USERNAME = sys.argv.pop()
        MyTest.PASSWORD = sys.argv.pop()
    unittest.main()
that will let you run with:

python mytests.py ausername apassword
You need the argv.pops so your command line params don't mess with unittest's own...

[update] The other thing you might want to look into is using environment variables:

import os
import unittest

class MyTest(unittest.TestCase):
    USERNAME = "jemima"
    PASSWORD = "password"

    def test_logins_or_something(self):
        print('username : {}'.format(self.USERNAME))
        print('password : {}'.format(self.PASSWORD))


if __name__ == "__main__":
    MyTest.USERNAME = os.environ.get('TEST_USERNAME', MyTest.USERNAME)            
    MyTest.PASSWORD = os.environ.get('TEST_PASSWORD', MyTest.PASSWORD)
    unittest.main()
That will let you run with:

TEST_USERNAME=ausername TEST_PASSWORD=apassword python mytests.py

''' 


def model_suite( dbh ):
	TestDaoDataMan.DBH = dbh
	
	suite = unittest.TestSuite()
	res = unittest.TestResult()
	suite.addTest( unittest.makeSuite( TestDaoDataMan ) )
	print( unittest.TextTestRunner(verbosity = 2).run(suite) )
 

try:

	DBData = {	'host' : 'localhost',
			'db' : 'comeandgo',
			'user' : 'root',
			'pw' : 't00rt00r'
	}

	dbm = DBMan( DBData )
	dbh = dbm.getDbh()
	
	model_suite( dbh )

except Exception as err:
	print('\n\n\n\n\n\nTESTSUITEERRRRRRRSUITEERR\n\n')
	print(err)

finally:
	dbh.rollback()
	
