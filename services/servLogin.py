import sys
import os
import pprint

import Cookie 

mypath = os.path.dirname( os.path.realpath(__file__) )

sys.path.append( mypath + '/../model/dto' )
#print( os.path.dirname( os.path.realpath(__file__) ) + '/../model/dto' )

import appuser
from appuser import * 

sys.path.append( mypath + '/../model' )

import DaoAuth
from DaoAuth import *

sys.path.append('/usr/local/lib/python2.7/dist-packages')

import random
from random import *

import md5
import json as simplejson
from django.http import HttpResponse

class ServLogin( object ):
	def __init__(self, env, start_response ):

                self.status = '200 OK'

                self.start_response = start_response
                self.env = env
                #pprint.pprint( self.env ) 

		C = Cookie.SimpleCookie()
		
		C['testcookie2'] = 'Testcookie2'
		C['testcookie2']['path'] = '/'
		C['testcookie2']['httponly'] = '1'
		C['testcookie2']['max-age'] = '+1d'
		C['testcookie'] = 'Testcookie'
		C['testcookie']['path'] = '/'
		C['testcookie']['httponly'] = '1'
		C['testcookie']['max-age'] = '+1d'
		
		#print( dir( C ) )
           
		self.resp_head = []	
		#h.extend( tuple( [ sessC.OutputString()[ :len( sessC.OutputString() ) - 1 ] ] ) for sessC in C.values()  )
		self.resp_head.extend( tuple( [ 'Set-Cookie', sessC.OutputString() ] ) for sessC in C.values()  )

		#self.resp_head.extend( tuple( [ 'Content-type', x ] ) for x in ['application/json'] ) 
		self.resp_head.append( tuple( [ 'Content-type', 'application/json' ] ) ) 

		print( list( self.resp_head ) )  

		self.response_headers = [
                        ('Set-Cookie', 'xoo=bar; path="/"'),
                        ('Set-Cookie', 'yoo=bar; path="/"'),
			( 'Content-Type', 'application/json' ) #,
                        #( 'Content-Length', str( len( output + ',RAISER : ' + '______________________________________') ) )
                ]


	def auth( self ):
		to_json = [ {
			"key1": "value1",
			"key2": "value2"
		} ]

		cred = { 'salt' : '12dF-09' }	
		for k in list( map( lambda x: x.split('='), self.env['QUERY_STRING'].split('&') ) ):
			cred[ k[0] ] = k[1]

		#print( cred )

		#pwstr = md5.new( cred['user'] + cred['password'] + cred['salt'] ).hexdigest()
		#print( pwstr )
		
		#print len( ( md5.new( ''.join( list( map( lambda x : chr( int( '7' + x ) ), str( random() ).replace( '.', '' ) ) ) ) ) ).hexdigest() )
		
		# generate a sid-string 
		#sid = md5.new( ''.join( list( map( lambda x : chr( int( '7' + x ) ), str( random() ).replace( '.', '' ) ) ) ) ).hexdigest()

		#usr = User( cred['user'], pwstr, sid )
		usr = User( cred['user'], cred['password'], 7 )

		#answ = daoAuth().addAppuser( usr )
		answ = daoAuth().startAuth( usr )
	
		print(dir(answ[0]))
		
		#raise Exception('nooooo')	
		ret = answ[0].getSid();
		rets =[] 
		
		#print(ret)
		#raise Exception 
		#if( length $logSucc <= 0 ){
		if( len( ret ) <= 0 ):
			ret = 0
			answ[0].setUsername('Wrongcredentials')
			
			rets.append( answ[0].getUsername() )
			
			'''
			rets = {
		               	'user' : answ[0].getUsername()
				#pw => $usr->accPasswordhash()
				#sid => $usr->accSid()
		       	}
			'''
		else :
			#answ[0].setSid( [ answ[0].getSid(), answ[0].getUsername() ] )
			'''
			rets = {	'user' : answ[0].getUsername(),
					'sid' : answ[0].getSid() 
		       	}
			'''
			map( lambda x : rets.append(x), [ answ[0].getSid(), answ[0].getUsername() ] )

			

		#print( dir( user ) )
		#print HttpResponse( simplejson.dumps(to_json), content_type='application/json' )
		#return HttpResponse( simplejson.dumps(to_json), content_type='application/json' )
		
		#self.start_response( self.status, self.response_headers )
		self.start_response( self.status, self.resp_head )
			
		self.output = simplejson.dumps( [ { 'rets' : rets } ] ) 
		#self.output = simplejson.dumps( rets ) 

		return self.output	
