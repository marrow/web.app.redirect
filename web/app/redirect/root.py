from web.dispatch.resource import Resource


class Redirect(Resource):
	def get(self):
		return "OK"
