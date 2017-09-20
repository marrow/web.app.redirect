"""Release information for the WebCore Redirection Service sample application."""

from collections import namedtuple

version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel', 'serial'))(1, 0, 0, 'final', 0)
version = ".".join([str(i) for i in version_info[:3]]) + \
		((version_info.releaselevel[0] + str(version_info.serial)) if version_info.releaselevel != 'final' else '')

author = namedtuple('Author', ['name', 'email'])("Alice Bevan-McGregor", 'alice@gothcandy.com')

description = "A sample reusable application component and isolated microservice to service domain redirections."
url = 'https://github.com/marrow/web.app.redirect/'
