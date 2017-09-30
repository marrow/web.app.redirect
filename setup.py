#!/usr/bin/env python3

import os
import sys
import codecs

try:
	from setuptools.core import setup, find_packages
except ImportError:
	from setuptools import setup, find_packages

if sys.version_info < (3, 4):
	raise SystemExit("Python 3.4 or later is required.")

version = description = url = author = ''  # Actually loaded on the next line; be quiet, linter.
exec(open(os.path.join("web", "app", "redirect", "release.py")).read())

here = os.path.abspath(os.path.dirname(__file__))

tests_require = [
		'pytest',  # test collector and extensible runner
		'pytest-cov',  # coverage reporting
		'pytest-flakes',  # syntax validation
		'pytest-catchlog',  # log capture
		'pytest-isort',  # import ordering
	]


setup(
	name = "web.app.redirect",
	version = version,
	description = description,
	long_description = codecs.open(os.path.join(here, 'README.rst'), 'r', 'utf8').read(),
	url = url,
	author = author.name,
	author_email = author.email,
	license = 'MIT',
	keywords = ['CleverCloud', 'webapp', 'sample', 'microservice', 'http', 'redirection', '302'],
	classifiers = [
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python",
			"Programming Language :: Python :: 3",
			"Programming Language :: Python :: 3.4",
			"Programming Language :: Python :: 3.5",
			"Programming Language :: Python :: 3.6",
			"Programming Language :: Python :: Implementation :: CPython",
			"Programming Language :: Python :: Implementation :: PyPy",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
	
	packages = find_packages(exclude=['test', 'example', 'benchmark', 'htmlcov']),
	include_package_data = True,
	package_data = {'': ['README.rst', 'LICENSE.txt']},
	namespace_packages = ['web', 'web.app'],
	zip_safe = False,
	
	setup_requires = [
			'pytest-runner',
		] if {'pytest', 'test', 'ptr'}.intersection(sys.argv) else [],
	
	install_requires = [
			'marrow.package>=1.1.0,<2.0.0',  # Plugin discovery and loading.
			'marrow.mongo[logger]>=1.1.2,<2.0.0',  # Database Access Object layer.
			'WebCore>=2.0.0,<3.0.0',  # Underlying web framework.
			'web.dispatch.resource>=2.0.0,<3.0.0',  # URL to endpoint lookup mechanism.
			'web.db>=2.0.1,<3.0.0',  # Framework integration for database access.
			'uri>=2.0.0,<3.0.0',  # Generic URI datastructure.
			'cinje>=1.1.0,<1.2.0',  # Template engine domain-specific language (DSL).
		],
	
	tests_require = tests_require,
	
	extras_require = dict(
			development = [
					'WebCore[development]>=2.0.0,<3.0.0',  # Underlying web framework with development dependencies.
					'pygments>=2.2.0,<2.3.0',  # Syntax highlighting of log output and cinje diagnostics.
					'waitress>=1.0.0,<1.1.0',  # "Production" quality WSGI HTTP front-end or "web server".
				],
			proxy = [  # Reverse proxy production deployments.
					'waitress>=1.0.0,<1.1.0',
				],
			uwsgi = [  # UWSGI production deployments.
					'uwsgi>=2.0.0,<2.1.0',
				],
			fcgi = [  # FastCGI production deployments.
					'flup6>=1.1.0,<1.2.0',
				]
		),
	
	entry_points = {
				'marrow.mongo.document': [  # Document classes registered by name.
						# 'RedirectionDomain = web.app.redirect.model:Domain',
					],
			},
)
