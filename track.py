class Track:
	""" This class depicts the data model. """
	def __init__(self, id, name, release_date, uri,duration,popularity):
			self.id = id
			self.name = name
			self.release_date = release_date
			self.uri = uri
			self.duration = duration
			self.popularity = popularity
	
	def as_tuple(self):
		return (self.id, self.name, self.release_date, self.uri, self.duration, self.popularity)