from web.dispatch.resource import Resource


class Root(Resource):
	def get(self):
		return "OK"
