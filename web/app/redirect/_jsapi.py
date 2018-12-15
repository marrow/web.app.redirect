from datetime import timedelta

from marrow.mongo import Document, Index
from marrow.mongo.field import Date, String, Integer, Mapping, Path, Alias, Link, Embed
from marrow.mongo.trait import Queryable, Published
from marrow.schema.validate.network import DNSName

from ._util import ReverseDNS


class APILink(Document):
	"""A JSON API link object.
	
	Primarily represented by an HTTP URL, however may be utilized as a dictionary to read/write additional metadata
	properties. May be subclassed to utilize a schema and attribute access for these application-spcific properties.
	"""
	
	href = Link(absolute=True, protocols={'http', 'https'})
	
	def __json__(self):
		"""A custom JSON representation for use within a JSON API response."""
		
		if len(self) > 1:
			meta = dict(self)
			href = meta.pop('href')
			
			return {'href': href, 'meta': meta}
		
		return self['href']


class Links(Document):
	"""Simplify construction of a JSON API "links object" due to use of Python reserved words.
	
	This aliases several names from the JSON representation to attributes more Python-friendly.
	"""
	
	obj = Embed(APILink, name='self')
	right = Embed(APILink, name='next')
	left = Embed(APILink, name='last')
	rel = Embed(APILink, name='related')
