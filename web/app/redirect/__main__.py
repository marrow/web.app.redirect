"""The WSGI application entry point.

Relevant environment variables:

MONGODB_ADDON_URI -- The mongodb:// URI to use as the primary connection, defaulting to localhost/test.
PORT -- The port the development server should bind to, defaulting to 8080.
PYTHON_OPTIMIZE -- Set this to enable optimizations, reduce logging level, and diable diagnostic aids.
"""

from os import getenv as ENV  # Configuration from the environment, ref: http://12factor.net/config

from web.core import Application  # WebCore WSGI Application base class.
from web.db.mongo import MongoDBConnection  # Redirection utilizes a MongoDB database.
from web.ext.analytics import AnalyticsExtension  # Some performance information.
from web.ext.db import DBExtension  # Generalized database adapter support.
from web.ext.serialize import SerializationExtension  # Simplified data serialization support.

if __debug__:
	from web.ext.debug import DebugExtension  # Development-time interactive debugger.

from web.app.redirect.root import Redirect  # The primary web-exposed entry point.


# This is our WSGI application instance.
app = Application(
		Redirect,
		
		extensions = [
				AnalyticsExtension(),
				SerializationExtension(),
				DBExtension(
						MongoDBConnection(
								ENV('MONGODB_ADDON_URI', "mongodb://localhost/test")
							)
					),
			] + ([
				DebugExtension()
			] if __debug__ else []),
		
		logging = {
				'version': 1,
				'handlers': {
						'console': {
								'class': 'logging.StreamHandler',
								'formatter': 'json',
								'level': 'DEBUG' if __debug__ else 'INFO',
								'stream': 'ext://sys.stdout',
							}
					},
				'loggers': {
						'web.app.redirect': {
								'level': 'DEBUG' if __debug__ else 'INFO',
								'handlers': ['console'],
								'propagate': False,
							},
						'web': {
								'level': 'DEBUG' if __debug__ else 'WARN',
								'handlers': ['console'],
								'propagate': False,
							},
					},
				'root': {
						'level': 'INFO' if __debug__ else 'WARN',
						'handlers': ['console']
					},
				'formatters': {
						'json': {'()': 'marrow.mongo.util.logger.JSONFormatter'}
					}
			}
		
	)


# If we're run as the "main script", serve our application over HTTP.
if __name__ == "__main__":
	app.serve(
			'wsgiref' if __debug__ else 'waitress',
			host = '127.0.0.1' if __debug__ else '0.0.0.0',
			port = int(ENV('PORT', 8080))
		)
