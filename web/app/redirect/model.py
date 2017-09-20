from datetime import timedelta

from marrow.mongo import Document, Index
from marrow.mongo.field import String, Integer, Mapping, Path, Alias, Link
from marrow.mongo.trait import Queryable

from .._util import ReverseDNS


class Redirection(Queryable):
	__collection__ = 'redirect'
	
	class Path(Document):
		__pk__ = 'source'
		
		source = Path()  # A source path to redirect, e.g. '/contact.php', '/company/about.aspx', etc.
		destination = Link()
		status = Integer(default=None)
	
	id = String('_id', transformer=ReverseDNS(), write=False)  # We override to use strings instead of ObjectIds.
	
	destination = Link(default=None)  # Default destination if no more specific destination can be resolved.
	status = Integer(default=301)  # Status code to utilize, see: https://httpstatuses.com
	path = Mapping(Path, key='source')  # Optional specific child redirections.
	
	domain = Alias('id')  # Convienence alias for legibility.
	
	_idx = Index('id', 'path.source')  # Optimize indexed lookup by path.
	_expire = Index('retracted', expire=timedelta(days=90).total_seconds(), sparse=True)  # Clean up expired data.
	
	def update_one(self, update=None, validate=True, **kw):
		"""Update this record, automatically tracking the modification time."""
		
		return super().update_one(update, validate, now__modified=True, **kw)
