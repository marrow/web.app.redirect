"""A collection of utilities utilized internally.

Please do not rely on these in your own code as they are subject to breaking change at any time.
"""

class ReverseDNS:
	def native(self, value, context):
		return '.'.join(value.split('.')[::-1])
	
	foreign = native
