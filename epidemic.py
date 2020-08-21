#! /usr/bin/python3

from urllib import request, parse, error
import json
from keys import *
from config import *
import base64
from track import Track
from dbcontext import DBContext
import os
from spotifywrapper import SpotifyWrapper
import logging


logging.basicConfig(filename="log.log",level=logging.DEBUG)


def read_tracks_file():
	"""
	Reads track id from flat file.
	:return: returns the content of the flat file.
	"""
	file_content = []
	if os.path.exists(tracks_file_name):
		try:
			with open(tracks_file_name) as tf:
				file_content = tf.readlines()
			
			file_content = [x.strip() for x in file_content] 
			logging.info("Track file read successfully.")
		except:
				logging.error("Cannot read tracks from file!")
				
	else:
		logging.error("Tracks file does not exist!")
		
	return file_content

		
def main():
	
	logging.info("Execution starterd.")
	logging.info("Reading track file.")
	### Read track IDs from flat file
	file_content = read_tracks_file()
	
	if file_content: 
		spotify_wrapper = SpotifyWrapper()
		### Fetch access token from Spotify
		logging.info("Authorizing with Spotify...")
		if spotify_wrapper.authorize():
			### Fetch song meta data
			logging.info("Fetching songs from Spotify...")
			tracks = spotify_wrapper.fetch_song_data(file_content)
			
			if tracks:
				### Create DB and Tracks table
				logging.info("Making sure DB table is created...")
				db_context = DBContext(database)
				db_context.create_table_tracks()
				
				### Write tracks to DB
				logging.info("Writing songs to DB...")
				for track in tracks["tracks"]:
					track_to_write= Track(track["id"],track["name"],track["album"]["release_date"],track["uri"],track["duration_ms"],track["popularity"])					
					db_context.insert_into_tracks(track_to_write)
						
				### Read tracks from DB
				logging.debug("Fetching songs from DB...")
				print("Fetching stored songs from DB...")
				for row in db_context.read_tracks():					
					logging.debug("Record found: ")
					logging.debug(row)
					print(row)
					
				
				
	


if __name__ == '__main__':
    main()