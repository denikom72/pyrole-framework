import pprint
import re

class Http(object):

	def __init__( self, queryStr ):
		self.setQStr( queryStr )
		print('\n\n\nINTO QUERYSTR\n\n\n')
		print( queryStr )

		print('\n\n\nINTO QUERYSTR\n\n\n')

	def setQStr( self, queryStr ):
		
		self.__qStr = {}
		
		''' PLAUSIBS '''	
		if( re.match( '.*&.*', queryStr ) ):
			qList = queryStr.split('&')
			
			for q in qList:
				self.__qStr[ q.split('=')[0].strip() ] = q.split('=')[1].strip()
		
		elif( re.match( '.*=.*', queryStr ) ):
			
			self.__qStr[ queryStr.split('=')[0].strip() ] = queryStr.split('=')[1].strip()
		
		else:	
			pass

		for x in [ '<', '>', '\'', '"', '%', '\\', '\r\n', '\n' ]:
			self.__qStr = dict( list( map( lambda k: tuple( [ k,  self.__qStr[k].replace( x, '' ) ] ), self.__qStr ) ) )
			

	def getQStr( self ):
		return self.__qStr
	

	def setCkies( self, cookies ):
		self.__ckies = cookies


	def getCkies( self ):
		return self.__ckies

	
	''' just an example '''
	def setBundle( self, queryStr, cookies ):
		self.setQStr( queryStr )
		self.setCkies( cookies )
		
		#important to return anonyme instances as method-params, cause constructor-overloading isn't possible
		return self

'''
Method 2: Using comrpehesion
# Initialization of dictionary 
dict = { 'Geeks': 10, 'for': 12, 'Geek': 31 } 
  
# Converting into list of tuple 
list = [ (k, v) for k, v in dict.items() ] 
  
Output:
[('Geek', 31), ('for', 12), ('Geeks', 10)]
 
Method #2 : Using items()
  
# Converting into list of tuple 
list = list(dict.items()) 
 
Method #3 : Using zip
  
# Using zip 
listt = zip(dict.keys(), dict.values()) 
  
# Converting from zip object to list object 
listt = list(listt) 
  

# Iteration 
for i in dict: 
   k = (i, dict[i]) 
   list.append(k) 
  
# Importing 
import collections 
  
# Converting 
list_of_tuple = collections.namedtuple('List', 'name value') 
  
lists = list(list_of_tuple(*item) for item in dict.items()) 
'''

#print str( Http('foo=muu&bar=n\nnar').getQStr() )
