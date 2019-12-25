import pprint 
import sys
import os

sys.path.append('/var/www/wsgi');

from mainCont import *
#reload( mainCont )

class Application(object):
	def __call__(self, environ, start_response):
		
		#ins = MainCont()
		
		fact = MainCont	
		
		self.route = {
			'' : fact.loginform,
			'/' : fact.loginform,
			'/applicationMan' : fact.appMan,
			'/applicationAdapter' : fact.servAppAdapt,
			'/doLogin' : fact.loginDone,
			'/servLogin' : fact.servLogin,
			'/servSearch' : fact.servSearch,
			'/servAddUser' : fact.servAddUser,
			'/servRoleMan' : fact.servRoleMan,
			'/jslib/basic.js' : 'jslib/basic.js',
			'/jslib/basic.css' : 'jslib/basic.css'
		}
		
		outp = 'EMPTY'	
		
		if( 'static' in environ['PATH_INFO'].split('/') ):
			print(environ['PATH_INFO'] + "\n\n\n\n\n")	
			currentPath = os.path.dirname(os.path.abspath(__file__) )
			print(os.path.join( currentPath, self.route[ environ['PATH_INFO'].replace( 'static/', '' ) ] ))
			f = open(os.path.join(currentPath, self.route[ environ['PATH_INFO'].replace( 'static/', '' ) ]), 'rb')
			
			print( dir( f ) )
			contnt = f.read()
			#print(contnt)	

			#headers = [('Content-Type', 'image/jpeg')]
			
			if( environ['PATH_INFO'].split('.')[-1] == 'js' ):
				conType = 'text/javascript; charset=utf-8'
			elif( environ['PATH_INFO'].split('.')[-1] == 'css' ):
				conType = 'text/css; charset=utf-8'

	
			headers = [	( 'Content-type', conType ),
					( 'Content-length', str( len( contnt ) ) )
			]


			start_response( '200 OK', headers )
			#myOutp = environ['wsgi.file_wrapper'](f, 32768)
			#myOutp = str( f.readlines() )
			#print( type( myOutp ) )
			myOutp = contnt	
			
			#myOutp = "{} ------- {}".format( conType, contnt )
		else:
			#print( '______ ' + environ['PATH_INFO'] )
		
			myOutp = self.route[ environ['PATH_INFO'] ]( environ, start_response )
		
		yield myOutp

''' IF USING AN APACHE-MODUL WSGI_MOD, THEN REMOVE COMMENT BEHIND THE NEXT SENTENCE/ROW AND MASK OR DELETE THE REST AFTER '''
#app = Application()


if __name__ == '__main__':
	
	from wsgiref.simple_server import make_server
    
	httpd = make_server( '', 8070, Application() )
	
	print('Serving on port 8070...')
	
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		print('Goodbye!')
