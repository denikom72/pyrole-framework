import pprint
import pdb

class DecDB(object):

	def __init__(self, dtoInst, stmnt = 'query' ):
        
		self.dtoInst = dtoInst
		self.stmnt = stmnt

	def __call__(self, fn, *args, **kwargs):

		def wrapper(*args, **kwargs):
			''' args[0] is self from wrapped function '''	
			print "function is decorated"
		
			
			this = args[0]
			pprint.pprint(args)
			print('\n\n\n\n\nKWARGS')
			pprint.pprint(fn(*args))	
			print('\n\n\n\n\nKWARGS')
			pprint.pprint( kwargs )	

			print(fn(*args))
			SQL = fn(*args)		
			
			if( 'testQuery' in kwargs and kwargs['testQuery'] != [] ):
				#print('\n\n\n\n\nSQL FOR APPEND\n\n\n')
				
				map( lambda x: SQL.append(x), kwargs['testQuery'] )
			'''
			else:
				SQL.append({ 'query': 'COMMIT', 'exec': [] })
			
				SQL.reverse()
				SQL.append({ 'query': 'START TRANSACTION', 'exec': [] })
				SQL.reverse()
			'''
			
			
			if( 'testQueryDto' in kwargs ):
				tQDto = kwargs['testQueryDto']
			
			
			if( 'test' not in kwargs or 'test' in kwargs and kwargs['test'] == False  ):
				
				SQL.append({ 'query': 'COMMIT', 'exec': [] })
			
				SQL.reverse()
				
				SQL.append({ 'query': 'START TRANSACTION', 'exec': [] })
				
				SQL.reverse()
			
			'''
			print( dir( this ) )	
			print( dir( self.dtoInst ) )	
			
			print "\n\n\nfunction is decorated\n\n\n"
			'''

			#print(fn(this))
			#SQL = fn(this)		
			

			#print( dir(SQL) )
			
			#map( lambda x: SQL.append(x),  )
				
			print(SQL)
		
			print('\n\n\n\n\n\nENDOFTHEUNIVERSE')
	
			#this.dbh.start_transaction()
	
			this.sth = this.dbh.cursor(buffered=True)
		
			res = []
			#this.sth.execute( 'START TRANSACTION', [] )

			def lmbd1(x):
				print(x['query'], ' __ ', x['exec'])
				res.append( this.sth.execute( x['query'], x['exec'], multi=True ) )
				print(' FOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO \n\n\n')
				pprint.pprint(res)

			#map( lambda x : res.append( this.sth.execute( x['query'], x['exec'], multi=True ) ), SQL ) 
			
			map( lambda x : lmbd1( x ), SQL ) 
			
			#raise Exception
			#this.sth.execute( kwargs['commOrRollb'], [] )
			
			print('\n\n\n\n\n\nENDOFTHEUNIVERSE')
			
			record = [] 	
			dtoList = []
			
			print( '\n\n\n\n\n\n INTRO INTO DECORATOR ')	
			
			try: 
				''' record is list of tuples '''
				#print(dir(this.sth))
				
				#test =True 
				
				if( self.stmnt == 'query' ):
					for ind in res:
						for curs in ind:
							print( 'Cursor: ', curs.with_rows )
							if curs.with_rows:
								record = this.sth.fetchall()
								print('\n\n\n\nQUERY')
								pprint.pprint(record)
								''' THIS FUNCTION MUST BE PASS AS A PARAM FROM THE WRAPPED METHOD, like lambda a, b, c: ... '''
								
								map( lambda x: dtoList.append( self.dtoInst( x ) ), record )
								#map( lambda x: dtoList.append( x ), record )
								print('\n\n\n\nENDQUERY')

				''' THIS CODE-PART IS NECESSARY TO WRITE UNIT-TESTS EASIER FOR models WITH CRUD-OPERATIONS '''
				#if( 'test' in kwargs and kwargs['test'] == True ):
				#if( 'test' in kwargs  ):
				for ind in res:
					for curs in ind:
						print( 'Cursor: ', curs.with_rows )
						if curs.with_rows:
							record = this.sth.fetchall()
							print('\n\n\n\nQUERY')
							pprint.pprint(record)
							''' THIS FUNCTION MUST BE PASS AS A PARAM FROM THE WRAPPED METHOD, like lambda a, b, c: ... '''
							
							map( lambda x: dtoList.append( tQDto( x ) ), record )
							#map( lambda x: dtoList.append( x ), record )
							print('\n\n\n\nENDQUERY')
						
				#this.dbh.rollback()
				print('\n\n\nDTOLISTTTTTTTTTTTTTT')
				pprint.pprint(dtoList)
				#this.dbh.commit()
	
	
			#except mysql.connector.Error as err:
			except Exception as err:
		        	print( 'DEC-ERROR : ' + str(err) )
				#this.dbh.rollback()
				record = []
			
			finally:
				''' closing database connection. '''
				if( this.dbh.is_connected() ):
					pass
					#this.sth.close()
			
			return( dtoList ) 
			
			'''
		        $sth->execute();
		
		       	my $res = $sth->fetchall_arrayref();
		
		        map {
		                 #ROLE ID, NAME, PRIORITY
		                 push( $listOfDto, Roles->new4( $_->[0], $_->[1], $_->[2] ) );
		        } @{ $res };
			'''
	
				#return fn(*args, **kwargs)
		return wrapper 

'''
@DecDB("arg1", "arg2")
def print_args_again(*args):
    for arg in args:
        print arg


print_args_again(1, 2, 3)
print_args_again(1, 2, 3)
'''
'''
def decorator(arg1, arg2):

    def real_decorator(function):

        def wrapper(*args, **kwargs):
            print "Congratulations.  You decorated a function that does something with %s and %s" % (arg1, arg2)
            function(*args, **kwargs)
        return wrapper

    return real_decorator


@decorator("arg1", "arg2")
def print_args(*args):
    for arg in args:
        print arg

And this sort of syntax is equivalent to:

def decorator(arg1, arg2):

    def real_decorator(function):

        def wrapper(*args, **kwargs):
            print "Congratulations.  You decorated a function that does something with %s and %s" % (arg1, arg2)
            function(*args, **kwargs)
        return wrapper

    return real_decorator


# No more decorator here
def print_args(*args):
    for arg in args:
        print arg


# getting crazy down here
decorator("arg1", "arg2")(print_args)(1, 2, 3)
Output
Congratulations.  You decorated a function that does something with arg1 and arg2
1
2
3
'''
