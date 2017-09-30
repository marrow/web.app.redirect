"""The WSGI application entry point.

Relevant environment variables:

PYTHON_OPTIMIZE -- Set this to enable optimizations, reduce logging level, and diable diagnostic aids.
MONGODB_ADDON_URI -- The mongodb:// URI to use as the primary connection, defaulting to localhost/test.
PORT -- The port the development server should bind to, defaulting to 8080.
"""

# Configuration from the environment, ref: http://12factor.net/config
from os import getenv as ENV

# Get a reference to the Application class.
from web.core import Application

# Simplified data serialization support.
from web.ext.serialize import SerializationExtension

# Generalized database adapter support.
from web.ext.db import DBExtension

# Redirection utilizes a MongoDB database.
from web.db.mongo import MongoDBConnection

if __debug__:
	from web.ext.analytics import AnalyticsExtension  # Some performance information.
	from web.ext.debug import DebugExtension  # Development-time interactive debugger.

# The primary web-exposed entry point.
from web.app.redirect.root import Redirect


# This is our WSGI application instance.
app = Application(
		Redirect,
		
		extensions = [
				SerializationExtension(),
				DBExtension(
						MongoDBConnection(
								ENV('MONGODB_ADDON_URI', "mongodb://localhost/test")
							)
					),
			] + ([
				AnalyticsExtension(),
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
