from webob import status_map as _STATUS

from web.dispatch.resource import Collection as _Collection
from marrow.mongo.query import Ops as _Ops

from ..resource.domain import Domain as _Domain


class Redirections(_Collection):
	"""A collection for the management of redirections on a per-domain basis."""
	
	__resource__ = _Domain
	
	def __getitem__(self, domain):
		"""Isolate the identifier for a child record."""
		
		return domain  # We pass-through the domain as-is; it's our identifier.
	
	def get(self, suffix=None, detail='none'):
		"""Retrieve an index of available domain redirections.
		
		Supports a few advanced HTTP features such as use of the `If-Modified-Since` header to request a listing of
		just those domains added or modified since the time given. Another mechanism for filtering is the `suffix`
		query string argument allowing for requesting a listing of a domain and all subdomains. E.g. with a suffix of
		`example.com` you might retrieve `example.com` and `www.example.com`.
		
		A specific level of detail may be requested. By default only the identifiers (domains) in the collection will
		be enumerated and returned. Supply a `detail` level of `domain` to retrieve whole Domain resources, and a
		level of `full` to retrieve Domain resources and their child paths. No pagination is offered, so full detail
		may contain a large amount of data.
		
		Results are sorted alphabetically in reverse DNS order. (`www.example.com` becomes `com.example.www`)
		
		# Success Responses
		
		* `200 OK` returning a JSON-API response.
		* `304 Not Modified` with no body if requesting records modified since a specific time and no records have been
			modified.
		
		# Failure Responses
		
		All failures except 500 return JSON-API error objects. The status code may vary based on the origin of failure:
		
		* `403 Forbidden` if you attempt to perform a suffix searh on a TLD.
		* `500 Internal Server Error` for any uncaught internal error.
		"""
		
		return {
				
			}
