import sys
import pprint

sys.path.append('/var/www/wsgi/model')

from DBMan import * 
from decDB import *

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

class DaoDataMan( object ):
	
	def __init__(self, dbh, roleProps):
	#def __init__(self, DBData, roleProps):
		self.sth = None	

		self.rlProp = roleProps
		print(self.rlProp.getPriorBehav())
		print(self.rlProp.getPrior())

		DBData = {	'host' : 'localhost',
				'db' : 'comeandgo',
				'user' : 'root',
				'pw' : 't00rt00r'
		}
	
		#dbm = DBMan( DBData )
		#self.dbh = dbm.getDbh()
		self.dbh = dbh
		print(dbh)	
	def priorFilt( self ):
        	#pprint.pprint self.rbac();
	        return " WHERE ( ( SELECT priority FROM roles WHERE name LIKE %s ) " + self.rlProp.getPriorBehav() + self.rlProp.getPrior() + " ) "


	def priorFiltSimple( self ): 
		return( self.rlProp.getPriorBehav() + " " + self.rlProp.getPrior() )
	
	
	def priorFilt2( self ):
        	return( " WHERE priority " + self.rlProp.getPriorBehav() + " " + str(self.rlProp.getPrior()) )


	def priorFilt3( self ): 
        	''' the WHERE-CLAUSEL HAS AN 'IF'-MEENING IN THIS CASE ''' 
		return " WHERE (  %s  "  + self.rlProp.getPriorBehav() + " " + str(self.rlProp.getPrior()) + " ) ";
	
	''' DAO-DTO-DECORATOR '''
	def daoDec( self, daoMethod, dtoInst ):
		
		print( '\n\n\n\n\n\n INTRO INTO DECORATOR ')	
		SQL = daoMethod()

		self.sth = self.dbh.cursor()
		
		map( lambda x : self.sth.execute( x['query'], x['exec'] ), SQL )
		
		record = [] 	
		
		dtoList = []
		print( '\n\n\n\n\n\n INTRO INTO DECORATOR ')	
		try: 
			record = self.sth.fetchall()
			pprint.pprint( record )

			'''
			# [ dtoList.append( RoleProps( x[0], x[1], x[2], x[3], x[4] ) ) for x in record ]

			for x in record :
				dtoList.append( RoleProps( x[0], x[1], x[2], x[3], x[4] ) )
			'''
			
			#map( lambda x : dtoList.append( RoleProps( x[0], x[1], x[2], x[3], x[4] ) ), self.sth.fetchall() )
		
			''' setRoleId returns the instance/self(this in other languages) '''
			'''
			def dtoInst(x):
				return RoleProps( 'placeholder', list(x)[1], list(x)[0] ).setRoleId( list(x)[2] ) 
			'''
			'''
			def myAppend( RoleProps ):
				dtoList.append( RoleProps )

			#map( lambda x : dtoList.append( RoleProps( 'placeholder', list(x)[1], list(x)[0] ).setRoleId( list(x)[2] ) ), record )
			def test( RoleProps, record ):
				map( lambda x : myAppend( dtoInst(x) ), record )
			
			test( RoleProps, record )
			'''	
			
			map( lambda x: dtoList.append( dtoInst(x) ), record )
			
	
			if(record):
				print(' RECORD : ')
				pprint.pprint( record )
			
			''' record is list of tuples '''

			#pprint.pprint( list( map( lambda x : [ list(x)[4].replace( 'lower', ' =================== ' ) or list(x)[4].replace('=', '_') ], record ) ) )
			#pprint.pprint( list( map( lambda x : [ x[4].replace( 'lower', ' =================== ' ) ], record ) ) )
			
			'''	
			for i in range( 0, len( record ) ) :
				#print(i)
				L = list( record[i] )
				L[4] = L[4].replace('lower', '<')
				L[4] = L[4].replace('equals:lower', '=<')
				record[i] = tuple( L )
			'''	

			self.dbh.commit()
		
		except mysql.connector.Error as err:
	        	print( 'SELROLE-ERROR : ' + err )
			self.dbh.rollback()
			record = []
		
		finally:
			''' closing database connection. '''
			if( self.dbh.is_connected() ):
		
				self.sth.close()
				#self.dbh.close()
				#print("connection is closed")
	
		#print( dir( dtoList[0] ) )
		#pprint.pprint( dtoList )
		
		return( dtoList ) 
		'''
	        $sth->execute();
	
	       	my $res = $sth->fetchall_arrayref();
	
	        map {
	                 #ROLE ID, NAME, PRIORITY
	                 push( $listOfDto, Roles->new4( $_->[0], $_->[1], $_->[2] ) );
	        } @{ $res };
		'''
	        
	
	def selRolesDump( self ):
		
		priorFlt2 = self.priorFilt2()
		
		def sqlDefs():
			SQL = [ {	
					'query': ''' SELECT * FROM roles ''' + priorFlt2 + ''' ORDER BY priority ASC ''',
					#'query': ''' SELECT * FROM roles  ORDER BY priority ASC ''',
					'exec': []
			} ]
			
			print( 'INTRO IN SQL-QUERIES' + priorFlt2 )
			
			return SQL	
		
		'''	
		def dtoInst(x):
			print(' \n\n\n\n\nINTO DTOINST\n\n\n')	
		
			#anonyme method doesn't need  return, lambda do it automatically
		
			return RoleProps( 'placeholder', list(x)[1], list(x)[0] ).setRoleId( list(x)[2] )
		'''

		return self.daoDec( sqlDefs, lambda x: RoleProps( 'placeholder', list(x)[1], list(x)[0] ).setRoleId( list(x)[2] ) )	
	
	
	@DecDB( lambda x: SearchRes( list(x)[0], list(x)[1], list(x)[2], list(x)[3], list(x)[4], list(x)[5], list(x)[6] ) )
	def listSearchRes( self, argObj ):
		#print('\n\n\nINTO DECORATED DEF\n\n\n\n\n\n')	
		return [ { 'query' : ''' SELECT 
					
					pers.name, 
			
					pers.surname, 
					
					COALESCE( pers.position, 'noPosition' ), 
					
					pers.email, 
					
					( SELECT name FROM roles WHERE id = usrol.roleId ) AS roName, 
					
					COALESCE( perscom.company_id, 'noCompany' ),
			
					( SELECT priority FROM roles AS ro WHERE id = usrol.roleId ) AS prior 
				FROM 
					users AS us
			
				LEFT JOIN 
					person AS pers ON us.email = pers.email
			
				LEFT JOIN 
					person_company AS perscom ON us.email = perscom.email
			
				LEFT JOIN 
					user_role AS usrol ON us.email = usrol.user
			
				 HAVING
			
					prior 
					 
					''' + self.priorFiltSimple() + '''
					
					AND

					( 
						pers.name LIKE %s OR pers.surname LIKE %s OR pers.email LIKE %s 
					);
			''',			
	
			'exec' :  [ argObj.getSearchStr(), argObj.getSearchStr(), argObj.getSearchStr() ]
			#'exec' :  [ 'test%', 'test%', 'test%' ]
		} ]

	
	
	@DecDB( lambda x: RoleProps( 'placeholder', list(x)[1], list(x)[0] ).setRoleId( list(x)[2] ) )
	def selRoles( self, testQuery = [], test = False ):
		#print('\n\n\nINTO DECORATED DEF\n\n\n\n\n\n')	
		return [ {	
				'query': ''' SELECT * FROM roles ''' + self.priorFilt2() + ''' ORDER BY priority ASC ''',
				#'query': ''' SELECT * FROM roles  ORDER BY priority ASC ''',
				'exec': []
		} ]

	
	@DecDB( lambda x: RoleProps( 'placeholder', 'placeholder', 'placeholder', 'placeholder', 'placeholder' ).setRoleId( list(x)[0] ) )
	def roleIdByRlName( self, rp ):
		
		#print('\n\n\nINTO DECORATED DEF\n\n\n\n\n\n')	
		#print(' SELECT id FROM roles ' + self.priorFilt2() + ' AND name LIKE  ')
		
		return [ {	
				'query': ''' SELECT id FROM roles ''' + self.priorFilt2() + ''' AND name LIKE %s ''',
				#'query': ''' SELECT * FROM roles  ORDER BY priority ASC ''',
				'exec': [ rp.getRolename() ]
		} ]

	def rIdDict( self ):
		self.dictRlId = {}

		def extDict( this, x ):
			this.dictRlId[ x.getRolename() ] = x.getRoleId()

		#map( lambda x: qStrRp.setRoleId( str( x.getRoleId() ) ) if x.getRolename() == qStr['selRole'] else True, self.selRoles() )
		map( lambda x: extDict( self, x ), self.selRoles() )
		
	
	@DecDB( lambda x:  RoleProps( list(x)[0], "placeholderForPrior", "placeHolderForRolename", "placeHolderForRoleuser", list(x)[1] ) )
	def selFuncsByRole( self, testQuery = [], test = False ):
		return [ {     'query': ''' 	SELECT ra.functionality, priorBehav AS func 
							
						FROM role_abil AS ra 
					
						WHERE ra.roleId = ( SELECT ro.id FROM roles AS ro WHERE ro.name LIKE %s ) ''',
                                'exec': [ self.rlProp.getRolename() ]
                } ]	
	
	        
	@DecDB( lambda x:  True, 'crud' )
	def addUser2Role( self, qStrRp , testQuery = [], testQueryDto = '', test = False ):
		
		parameter = ' roleId, user '

		EXEC = [ qStrRp.getRoleId(), qStrRp.getRoleUser(), self.rlProp.getRolename() ]
	        
		return [ {	'query': ''' 
					INSERT INTO user_role(''' + parameter + ''')

					SELECT d.* FROM (
						SELECT
							%s AS 'rId',
							%s AS 'usr'
					) AS d

					''' + self.priorFilt() + '''

					ON DUPLICATE KEY UPDATE roleId = d.rId, user = d.usr 
				''',

				'exec': EXEC 
		} ]

	@DecDB( lambda x:  True, 'crud' )
	def addUser( self, appuser, testQuery = [], testQueryDto = '', test = False ):

		parameter = 'email, passwordhash'	
		
		EXEC = [ appuser.getUsername(), appuser.getPwd() ]
		
		return [ {	'query': ''' INSERT INTO users ( '''  + parameter + ''' ) VALUES ( %s, %s ) ''',

				'exec': EXEC 
			}
		]

	


	@DecDB( lambda x:  True, 'crud' )
	def addRole( self, qStrRl ):
		parameter = 'name, priority'	
		
		EXEC = [ qStrRl.getRolename(), qStrRl.getPrior(), qStrRl.getPrior(), qStrRl.getPrior() ]
	        
		return [ {	'query': ''' 
					INSERT INTO roles(''' + parameter + ''') 
        
			                SELECT d.* FROM (
                        			SELECT
			                        %s AS 'name',
                        			%s AS 'prior'
			                ) AS d

		                ''' + self.priorFilt3() + '''
                
                		ON DUPLICATE KEY UPDATE priority = %s
				''',

				'exec': EXEC 
		} ]
	
	
	@DecDB( lambda x:  True, 'crud' )
	def addPerson( self, pers, testQuery = [], testQueryDto = '', test = False ):
		parameter = 'name, surname, position, email'	

		EXEC = [ pers.getName(), pers.getSurname(), pers.getPosition(), pers.getEmail() ]
		
		return [ {	'query': ''' INSERT INTO person ( '''  + parameter + ''' ) VALUES ( %s, %s, %s, %s ) ''',

				'exec': EXEC 
		} ]

	
	@DecDB( lambda x:  True, 'crud' )
	def adaptApplic( self, testQuery = [], testQueryDto = '', test = False  ):

		parameter = 'roleId, functionality, priorBehav'	

		if( self.rlProp.getPriorBehav() == 'NLL' or self.rlProp.getPriorBehav() == '' ):
			behav = 'NULL'
		else:
			behav = "\'" + self.rlProp.getPriorBehav() + "\'"

		EXEC = [ self.rlProp.getFunct(), self.rlProp.getRolename(), self.rlProp.getPriorBehav() ]
		
		if( not self.rlProp.getPriorBehav() ):
			self.rlProp.setPriorBehav('NLL')
	    	    
		return [ {	'query': ''' 
					INSERT INTO
					                        
					                role_abil( ''' +  parameter + ''' )
					                        
					        SELECT ro.id AS rid, %s AS roFunc, ''' +  behav + ''' AS roPriorBehav 
					                
					                FROM roles AS ro
					                        
					        WHERE ro.name
					                        
					                LIKE %s
					
					        ON DUPLICATE KEY UPDATE
					
					                priorBehav = ''' + behav  + ''', functionality = %s
					''',

				'exec': EXEC 
		} ]

	
	@DecDB( lambda x:  True, 'crud' )
	def removeFuncFromRole( self ):

		EXEC = [ self.rlProp.getFunct(), self.rlProp.getRolename() ]
		
		return [ {	'query': ''' 
					DELETE FROM role_abil WHERE functionality LIKE %s 

					AND 

					roleId = ( SELECT ro.id FROM roles AS ro WHERE ro.name LIKE %s )
					''',

				'exec': EXEC 
		} ]


'''
sub adaptApplic {
	my $self = shift;
	my ( $rolAb, $rol ) = ( shift, shift );

	my $parameter = 'roleId, functionality, priorBehav';
	#my $values = '?, ?, ?';
	
	my @EXECUTE2 = ( $rolAb->accFunctionality(), $rolAb->accPriorBehav(), $rolAb->accPriorBehav(), $rol->accName(), $rolAb->accPriorBehav(), $rolAb->accPriorBehav(),$rolAb->accFunctionality() );
	
	my @EXECUTE = ( $rolAb->accFunctionality(), $rol->accName(), $rolAb->accFunctionality() );

	my $behav = $rolAb->accPriorBehav() eq 'NLL' || $rolAb->accPriorBehav() eq '' ? 'NULL' : "\'" . $rolAb->accPriorBehav() . "\'";

	if( !$rolAb->accPriorBehav() ){
		$rolAb->accPriorBehav('NLL');
	}

	my $sql = ' 
	
	INSERT INTO
			
		role_abil( ' . $parameter . ' )
			
	SELECT ro.id AS rid, ? AS roFunc, ' . $behav . ' AS roPriorBehav 
		
		FROM roles AS ro
			
	WHERE ro.name
			
	        LIKE ?

	ON DUPLICATE KEY UPDATE

		priorBehav = ' . $behav  . ', functionality = ?;
	';
	
	# ifnull, nullif, COALESCE( NULLIF(phone, ''), bar, xoo )  AS foo

	
	try {
		
	
		#cause MYSQL has problems with empty strings and convert NULL inserts into 0 or '', here will just be fired a die
		die(' EMPTY BEHAVIOUR-CONDITION ') if $behav eq 'NULL';
		my $sth = $self->{'dbh'}->prepare($sql);
		$sth->execute(@EXECUTE);
		
	} catch {
		warn " --- ADAPT-APPLICATION-ERROR ::::::: " . $_ ." -- " . $sth->errstr;
		$_;	
	}
	
}
'''
	
''' TESTS '''


''' TEST WITH WRONG CREDENTIALS ''' 
#DaoSess(DBData).checkSessID( User('py3user@test.com', 'f9857e0fc56612db6d961200cd0e39bf', 'd99e159d290d7eaf244bb9310acb6') )
#DaoSess().rbacProps( User('py3user@test.com', 'f9857e0fc56612db6d961200cd0e39bf', 'd99e159d290d7eaf244bb9310acb6') )

#import roleProps
#from roleProps import * 

''' TEST WITH RIGHT CREDENTIALS ''' 
#usr = User('py4user@test.com', 'badpw123xy', '7')
#DaoSess(DBData).checkSessID( usr )
#DaoSess().rbacProps( usr )



#pers = Person('pers1', 'surname1', 'manager', 'nomail2@ml.com')
#rp = RoleProps('somefnc', '200', 'admin', 'py4user@test.com', 'equals:lower')
#appuser = User('nomail2@ml.com', 'f9857e0fc56612db6d961200cd0e39bf')
#rp.setRoleId(2)

#pprint.pprint( DaoDataMan({'foo':'bar'}, rp).listSearchRes( SearchDt('test%') ) )


''' ADDUSER TEST '''
#pprint.pprint( DaoDataMan( {'foo':'bar'}, rp ).addUser( appuser ) )
#pprint.pprint( DaoDataMan( {'foo':'bar'}, rp ).addPerson( pers ) )
#pprint.pprint( DaoDataMan( {'foo':'bar'}, rp ).addUser2Role() )
''' ADDUSERTEST END '''


#pprint.pprint( DaoDataMan({'foo':'bar'}, rp).adaptApplic() )
#pprint.pprint( DaoDataMan({'foo':'bar'}, rp ).removeFuncFromRole() )

#pprint.pprint( DaoDataMan({'foo':'bar'}, rp).selRoles() )
#pprint.pprint( DaoDataMan({'foo':'bar'}, rp).roleIdByRlName('manager') )
#print("MODELTEST-SELFUNCBYROLE\n\n\n\n\n\n")
#pprint.pprint( DaoDataMan({'foo':'bar'}, rp).selFuncsByRole() )
#print( RoleProps( 'placeholder', 'list', 'list', 'list' ).getRolename() )

#print("END MODELTEST")
