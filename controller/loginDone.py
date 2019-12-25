#from pythonlangutil.overload import Overload, signature
import sys
import os

sys.path.append('/usr/local/lib/python2.7/dist-packages')

import django

from django import template   
from django.template.loader import get_template
from django.template import Template, Context

class LoginDone( object ):
	def __init__(self, env, start_response ):
		
		self.status = '200 OK'
		
		self.start_response = start_response
		self.env = env
		#pprint.pprint( self.env ) 

		self.response_headers = [
                        ( 'Content-type', 'text/html' ) #,
                        #( 'Content-Length', str( len( output + ',RAISER : ' + '______________________________________') ) )
	        ]

	def tpl( self ):
		
		#t = get_template('login.html')
		self.start_response( self.status, self.response_headers )
		#self.output = str( t.render() )
		self.output = b'New Output' 

		return self.output
