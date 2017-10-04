from datetime import timedelta

from marrow.mongo import Document, Index
from marrow.mongo.field import Date, String, Integer, Mapping, Path, Alias, Link, Embed
from marrow.mongo.trait import Queryable, Published
from marrow.schema.validate.network import DNSName

from ._util import ReverseDNS


class Redirection(Published, Queryable):
	__collection__ = 'redirect'
	
	class Map(Document):
		__pk__ = 'source'
		
		source = Path()  # A source path to redirect, e.g. '/contact.php', '/company/about.aspx', etc.
		destination = Link()  # The full URL to redirect to, or a fragment to resolve against Redirection.destination.
		status = Integer(default=None)  # The specific integer HTTP status code to utilize for this source path.
	
	# Store domains in reverse order, e.g.: com.example.www
	id = String('_id', transformer=ReverseDNS(), validator=DNSName(), write=False)
	
	destination = Link(default=None)  # Default destination if no more specific destination can be resolved.
	status = Integer(default=301)  # Status code to utilize, see: https://httpstatuses.com
	path = Mapping(Map, key=Map.__pk__)  # Optional specific child redirections.
	
	# Creation, modification, publication, and retractioon dates are included via the `Published` trait.
	verified = Date(default=None)  # The date/time of verification.
	
	domain = Alias('id')  # Convienence alias for legibility.
	
	_idx = Index('id', 'path.source')  # Optimize indexed lookup by path.
	_expire = Index('retracted', expire=timedelta(days=90).total_seconds(), sparse=True)  # Clean up expired data.
	
	def update_one(self, update=None, validate=True, **kw):
		"""Update this record, automatically tracking the modification time."""
		
		return super().update_one(update, validate, now__modified=True, **kw)
