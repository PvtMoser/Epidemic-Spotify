from keys import *
import base64
import json
from urllib import request, parse, error
import logging

class SpotifyWrapper:
	""" This class wraps the Spotify API interactions """

	def __init__(self):
		self.client_id = client_id
		self.client_secret = client_secret
		
	def authorize(self):
		"""
		Authorize with Spotify API and fetch bearer token.
		:return: Returns true if successful, otherwise false.
		"""
		try:
			auth_url = 'https://accounts.spotify.com/api/token'
			headers={}
			data={}

			data_string = f"{self.client_id}:{self.client_secret}"

			data_bytes = data_string.encode("ascii")
			base_bytes = base64.b64encode(data_bytes)
			base_message = base_bytes.decode("ascii")

			headers['Authorization'] = f"Basic {base_message}"

			data = parse.urlencode({"grant_type": "client_credentials"})
			data = data.encode('ascii')

			req = request.Request(auth_url,data=data, headers=headers)
			logging.info("Successfully called Spotify token API!")
		except:
			logging.error("Failed to create authorization request!")
			return False
			
		if req is not None:
			try:
				response = request.urlopen(req).read().decode()
			except error.URLError as e:
				response = e.read().decode("utf8", 'ignore')
				logging.error(response)
				return False
		
		try:
			_json = json.loads(response)
			self.token = _json["access_token"]
			logging.info("Successfully received token from Spotify!")
		except:
			logging.error("Could not fetch token from response!")
			return False
			
		return True
		
	def fetch_song_data(self, song_ids):
		"""
		Fetch song meta data from Spotify API
		:param song_ids: list of track ids.
		:return: returns dict of track meta data. 
		"""
		tracks_base_url = "https://api.spotify.com/v1/tracks"
		headers = {}
		track_ids = ','.join(song_ids)
		query_params = "/?ids="+track_ids
		tracks_url = tracks_base_url + query_params
		tracks={}
		headers['Authorization'] = f"Bearer {self.token}"

		try:
			req = request.Request(url=tracks_url,data=None, headers=headers)
			response = request.urlopen(req).read().decode()
			tracks = json.loads(response)
			logging.info("Successfully fetched songs from Spotify!")
		except error.URLError as e:
			response = e.read().decode("utf8", 'ignore')
			logging.error(response)
		return tracks