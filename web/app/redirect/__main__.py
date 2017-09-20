import os

# Get a reference to the Application class.
from web.core import Application

# Some performance information.
from web.ext.analytics import AnalyticsExtension

# Simplified data serialization support.
from web.ext.serialize import SerializationExtension

# Generalized database adapter support.
from web.ext.db import DBExtension

# Redirection utilizes a MongoDB database.
from web.db.mongo import MongoDBConnection

if __debug__:  # Development-time interactive debugger.
	from web.ext.debug import DebugExtension

# The primary web-exposed entry point.
from web.app.redirect.root import Redirect


# This is our WSGI application instance.
app = Application(
		Redirect,
		
		extensions = [
				AnalyticsExtension(),
				SerializationExtension(),
				DBExtension(
						MongoDBConnection(
								os.environ.get('MONGODB_ADDON_URI', "mongodb://localhost/test")
							)
					),
			] + ([DebugExtension()] if __debug__ else []),
		
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
			port = os.environ.get('MONGODB_ADDON_URI', "mongodb://localhost/test")
		)
