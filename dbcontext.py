import sqlite3
from sqlite3 import Error
import time
import logging

class DBContext:
	""" This class wraps the DB interactions """
	def __init__(self, db_file):
		self.create_connection(db_file)
	
	def create_connection(self, db_file):
		""" create a database connection to the SQLite database
        specified by db_file
		:param db_file: database file
		:return: Returns connection object.
		"""
		self.conn = None
		try:
			self.conn = sqlite3.connect(db_file)
			logging.info("Successfully connected to DB.")
		except Error as e:
			logging.error(e)
		return self.conn
			
	def commit(self, statement, params=None):
		""" executes and commits an SQL statment
		:param statement: the SQL statement to be executed
		:params: potentially used variables to be inserted into the SQL statement.
		"""
		if self.conn is not None:
			### retry the commit a few times
			for x in range (0, 10):
				try:
					c = self.conn.cursor()
					if params:
						c.execute(statement, params)
					else:
						c.execute(statement)
					self.conn.commit()
					logging.info("Successfully committed to DB.")
				except Error as e:
					time.sleep(1)
					pass
				finally:
					break
			### final else to return the error code
			else:
				try:
					c = self.conn.cursor()
					if params:
						c.execute(statement, params)
					else:
						c.execute(statement)
					self.conn.commit()
				except Error as e:
					logging.error(e)
				
		else:
			print("Error! cannot create the database connection.")
		
	def create_table_tracks(self):
		""" create a table from the create_table_sql statement
		"""
		logging.info("Creating DB table if does not exist...")
		create_table_sql = """ CREATE TABLE IF NOT EXISTS tracks (
									id text PRIMARY KEY, 
									name text NOT NULL, 
									release_date text, 
									uri text, 
									duration integer, 
									popularity integer); """
		self.commit(create_table_sql)
		
			
	def insert_into_tracks(self, track):
		"""
		Create a new track
		:param conn:
		:param track:
		"""
		if track:
			logging.debug("Writing song "+ track.name + "...")
			sql = ''' INSERT OR REPLACE INTO tracks(id,name,release_date,uri,duration,popularity)
					  VALUES(?,?,?,?,?,?) '''
			
			self.commit(sql, track.as_tuple())		

			
	def read_tracks(self):
		"""
		Read all tracks
		"""
				  
		if self.conn is not None:
			try:
				cur = self.conn.cursor()
				cur.execute("SELECT * FROM tracks")
				rows = cur.fetchall()
				return rows
			except Error as e:
				print(e)
		else:
			print("Error! cannot create the database connection.")